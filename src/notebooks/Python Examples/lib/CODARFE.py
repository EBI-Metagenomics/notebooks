import zipfile
import shutil
import os
import sys
import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.linalg import svd
import math
import operator

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import HuberRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split

import pickle as pk
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as colors
from IPython.display import HTML, display
from typing import Optional, Tuple, Union

import warnings
warnings.filterwarnings("ignore")

class CODARFE():
  """
  This class implements a microbiome analysis tool and prediction of continuous environmental variables associated with the microbiome.
  It utilizes the RFE method combined with robust-to-noise regression, CoDA analysis, and 4 metrics for selecting a subgroup of the microbiome highly associated with the target variable.
  As a result, CODARFE can predict the target variable in new microbiome samples.

  CODARFE requires the following parameters:

    data: pd.DataFrame = None
          DataFrame containing count data (microbiome);
    metaData: pd.DataFrame = None
          DataFrame containing the target variable related to the microbiome;
    metaData_target: str = None
          Name of the column in metaData that contains the target variable.

  Usage:
      1) Create an instance of CODARFE with your data:

      coda = CODARFE(data       = <microbiome_dataframe>,
                     metaData   = <metadata_dataframe>,
                     metaData_Target = <string_target_variable_name>)

      2) Train a model:

      coda.CreateModel( write_results            = True,
                        path_out                 = '',
                        name_append              = '',
                        rLowVar                  = True,
                        applyAbunRel             = True,
                        percentage_cols_2_remove = 1,
                        n_Kfold_CV               = 10,
                        weightR2                 = 1.0,
                        weightProbF              = 0.5,
                        weightBIC                = 1.0,
                        weightRMSE               = 1.5,
                        n_max_iter_huber         = 100
                     )


      3) Save the model:

      coda.Save_Instance(path_out    = <path_to_folder>,
                         name_append = <name>)


      Alternatively, you can load a pre-trained model

      
      coda = CODARFE()
      coda.Load_Instance(path2instance = <path_to_file_instance.foda>)
     


      4) View the results:

        4.1) Plot of predicted vs. expected correlation

        coda.Plot_Correlation(path_out    = <path_to_folder>,
                              name_append = <name>)

        4.2) Plot the mean absolute error using a hold-out validation

        coda.Plot_HoldOut_Validation( n_repetitions = 100,
                                      test_size     = 20,
                                      path_out      = <path_to_folder>,
                                      name_append   = <name>)

        4.3) Plot of the relationship of predictors with the target

        coda.Plot_Relevant_Predictors(n_max_features = 100,
                                      path_out       = <path_to_folder>,
                                      name_append    = <name>)

        4.4) Heatmap of selected predictors

        coda.Plot_Heatmap(path_out    = <path_to_folder>,
                          name_append = <name>)

        4.5) Selected predictors

        coda.selected_taxa

      5) Predict the target variable in new samples:

      coda.Predict( path2newdata = <path_to_new_data>,
                    applyAbunRel = True,
                    writeResults = True,
                    path_out     = <path_out>
                    name_append  = <name>)

  For more information about the tool, visit the original publication or the GitHub containing more versions of this same tool.

  For questions, suggestions, or bug/error reports, contact via email: murilobarbosa@alunos.utfpr.edu.br"

  """
  class ModelNotCreatedError(Exception):
    def __init__(self, mensagem="No model created! Please create the model using the CreateModel function and try again."):
            self.mensagem = mensagem
            super().__init__(self.mensagem)

  class EmptyDataError(Exception):
    def __init__(self, mensagem="No model created! Please create the model using the CreateModel function and try again."):
            self.mensagem = mensagem
            super().__init__(self.mensagem)
            
  class LowFitModelWarning(UserWarning):
    pass
 
  class NotSignificantPvalueWarning(UserWarning):
    pass

  class LowRateOfSelectedPresentWarning(UserWarning):
    pass

  class ImpossibleToGeneralizeWarning(UserWarning):
    pass


  def __init__(self,
               data: Optional[pd.DataFrame] = None,
               metaData: Optional[pd.DataFrame] = None,
               metaData_Target: Optional[str] = None) -> None:
    """
    Parameters
    ----------
    data: pd.DataFrame = None
          The microbiome dataframe (counting table)
    metaData: pd.DataFrame = None
          The metadata dataframe with the target variable
    metaData_Target: str = None
          The name of the target variable column inside the metadata 
    """

    self.__metaData = metaData
    if (type(data) != type(None)) and (type(metaData) != type(None)) and (type(metaData_Target) != type(None)):
      #print("Loading data... It may take some minutes depending on the size of the data")
      self.data, self.target = self.__Read_Data(data,metaData,metaData_Target)
      self.__totalPredictorsInDatabase = len(self.data.columns)
    else:
      self.data = None
      self.target = None
      # print('No complete data provided. Please use the function Load_Instance(<path_2_instance>) to load an already created CODARFE model.')

    self.__sqrt_transform = None
    self.__transform = None
    self.__min_target_sqrt_transformed = None
    self.__max_target_sqrt_transformed = None
    self.__min_target_transformed = None
    self.__max_target_transformed = None
    self.results = None
    self.score_best_model = None
    self.selected_taxa = None
    self.__model = None
    self.__n_max_iter_huber = None

    self.__correlation_list = {}

  def __Read_Data(self,data,metadata,target_column_name):

    totTotal = len(metadata)
    if target_column_name not in metadata.columns:
      print("The Target is not present in the metadata table!")
      sys.exit(1)
    totNotNa = metadata[target_column_name].isna().sum()
    metadata.dropna(subset=[target_column_name],axis=0,inplace=True)

    indxs = [idx for idx in metadata.index if idx in data.index]
    data = data.loc[indxs]
    y = metadata.loc[indxs][target_column_name]

    if len(data) == 0:
      print('There is no correspondence between the ids of the predictors and the metadata.\nMake sure the column corresponding to the identifiers is first.')
      sys.exit(1)
    print('Total samples with the target variable: ',totTotal-totNotNa,'/',totTotal)

    return data,y

  def Save_Instance(self,path_out: str,name_append: Optional[str]='CODARFE_MODEL') -> None:
    """
    Parameters
    ----------
    path_out: str
              Path to folder where it will be saved. If no path is provided it will save in the same directory as the metadata with the name of 'CODARFE_MODEL.foda'
    name_append: str = 'CODARFE_MODEL'
              Name to concatenate in the final filename.

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
              If de path_out does not exists

    """
    if type(self.data) == type(None):
      print('Nothing to save.')
      return

    if '/' in path_out:
      path2 = '/'.join(path_out.split('/')[:-1])
      if not os.path.exists(path2):
        raise FileNotFoundError("The path out does not exists!")

    obj = {'data':self.data,
           'target':self.target,
           'sqrt_transform': self.__sqrt_transform,
           'transform': self.__transform,
           'min_target_sqrt_transformed': self.__min_target_sqrt_transformed,
           'max_target_sqrt_transformed': self.__max_target_sqrt_transformed,
           'min_target_transformed': self.__min_target_transformed,
           'max_target_transformed': self.__max_target_transformed,
           'results': self.results,
           'score_best_model': self.score_best_model,
           'selected_taxa': self.selected_taxa,
           'model': self.__model,
           'n_max_iter_huber': self.__n_max_iter_huber,
           'correlation_list':self.__correlation_list}

    name = path_out+name_append
    with open(name+'.foda','wb') as f:
      pk.dump(obj,f)

    print('\n\nInstance saved at ',name+'.foda\n\n')

  def Load_Instance(self,path2instance: str) -> None:
    """
    Load the CODARFE instance stored in the <path2instance> file into this object.

    Parameters
    ----------
    path2instance: str
                   Path to ".foda" file

    Returns
    ------
    None

    Raises
    ------
    FileNotFoundError
                   If the path2instance does not exists

    """
    if not os.path.exists(path2instance):
      raise FileNotFoundError(f"The file {path2instance} does not exists")

    with open(path2instance,'rb') as f:
      obj = pk.load(f)


    self.data = obj['data']
    self.target = obj['target']
    self.__sqrt_transform = obj['sqrt_transform']
    self.__transform = obj['transform']
    self.__min_target_sqrt_transformed = obj['min_target_sqrt_transformed']
    self.__max_target_sqrt_transformed = obj['max_target_sqrt_transformed']
    self.__min_target_transformed = obj['min_target_transformed']
    self.__max_target_transformed = obj['max_target_transformed']
    self.results = obj['results']
    self.score_best_model = obj['score_best_model']
    self.selected_taxa = obj['selected_taxa']
    self.__model = obj['model']
    self.__n_max_iter_huber = obj['n_max_iter_huber']
    self.__correlation_list = obj['correlation_list']

    print('\n\nInstance restored successfully!\n\n')


  def __removeLowVar(self):
    aux = self.data.copy()
    cols = aux.columns
    selector = VarianceThreshold(aux.var(axis=0).mean()/8)#8
    aux = selector.fit(aux)
    not_to_drop=list(cols[selector.get_support()])
    totRemoved = len(self.data.columns) - len(not_to_drop)
    print('\nA total of ',totRemoved,' predictors were removed due to very low variance\n')
    self.data =  self.data[not_to_drop]

  def __toAbunRel(self,data):
    return data.apply(lambda x: x/x.sum() if x.sum()!=0 else x,axis=1)

  def __calc_new_redimension(self,target):

    minimo = min(target)
    maximo = max(target)
    if self.__min_target_transformed == None or self.__max_target_transformed == None:
      self.__min_target_transformed = minimo
      self.__max_target_transformed = maximo

    numeros_redimensionados = [x + abs(self.__min_target_transformed)+1 for x in target]
    return numeros_redimensionados
  
  def __calc_inverse_redimension(self,predictions):

    numeros_restaurados = [x - abs(self.__min_target_transformed)-1 for x in predictions]

    return numeros_restaurados

  def __calc_new_sqrt_redimension(self,target):
    target = target.apply(lambda x: np.sqrt(abs(x)) * (-1 if x < 0 else 1))

    minimo = min(target)
    maximo = max(target)
    if self.__min_target_sqrt_transformed == None or self.__max_target_sqrt_transformed == None:
      self.__min_target_sqrt_transformed = minimo
      self.__max_target_sqrt_transformed = maximo

    # numeros_redimensionados = [x + abs(self.__min_target_sqrt_transformed)+1 for x in target]
    new_min = 0  # novo valor mínimo desejado
    new_max = 100  # novo valor máximo desejado

    numeros_redimensionados = [(x - minimo) / (maximo - minimo) * (new_max - new_min) + new_min for x in target]
    return numeros_redimensionados

  def __calc_inverse_sqrt_redimension(self,predictions):
    new_min = 0  # novo valor mínimo usado na transformação
    new_max = 100  # novo valor máximo usado na transformação

    minimo = self.__min_target_sqrt_transformed
    maximo = self.__max_target_sqrt_transformed

    # numeros_restaurados = [x + abs(self.__min_target_sqrt_transformed)+1 for x in predictions]
    numeros_restaurados = [(x - new_min) / (new_max - new_min) * (maximo - minimo) + minimo for x in predictions]
    numeros_restaurados_sqrt_inverse = [(x**2) * (-1 if x <0 else 1) for x in numeros_restaurados]
    return numeros_restaurados_sqrt_inverse

  def __toCLR(self,df): # Transform to CLr
    aux = df.copy()
    aux+=0.0001 # Pseudo count
    aux = aux.apply(lambda x: np.log(x/np.exp(np.log(x).mean())),axis=1)
    return aux

  def __calc_mse_model_centeredv2(self,pred,y,df_model): #pred é o valor predito  # df_model é o número de variáveis
    mean = np.mean(y)
    ssr = sum([(yy-pp)**2 for yy,pp in zip(y,pred)])
    centered_tss = sum([(aux-mean)**2 for aux in y])
    ess = centered_tss - ssr
    return ess/df_model

  def __calc_mse_resid(self,pred,y,df_resid):
    residuos = [yy-pp for yy,pp in zip(y,pred)]
    return sum([aux**2 for aux in residuos])/df_resid

  def __calc_f_prob_centeredv2(self,pred,y,X):
    df_model = max(1,len(X.iloc[0]) - 1)
    df_resid = max(1,len(X) - df_model -1 )
    mse_model = self.__calc_mse_model_centeredv2(pred,y,df_model)
    mse_resid = self.__calc_mse_resid(pred,y,df_resid)
    fstatistic = mse_model/mse_resid
    return stats.f.sf(fstatistic, df_model, df_resid)

  def __calc_r_squared(self,pred,y,method = 'centered'):
    ssr = sum([(yy-pp)**2 for yy,pp in zip(y,pred)])
    mean = np.mean(y)
    center_tss = np.sum((y - mean)**2)
    uncentered_tss = sum([(aux)**2 for aux in y])
    if method == 'centered':
      return 1 - ssr/center_tss
    else:
      return 1 - ssr/uncentered_tss

  def __calc_rsquared_adj(self,X,r2):
    return 1 - (1-r2) * (X.shape[0]-1)/(X.shape[0]-X.shape[1]-1)

  def __calc_llf(self,pred,y,X):
    nobs2 = len(X) / 2.0
    nobs = float(len(X))
    ssr = sum([(yy-pp)**2 for yy,pp in zip(y,pred)])
    llf = -nobs2*np.log(2*np.pi) - nobs2*np.log(ssr / nobs) - nobs2
    return llf


  def __calc_bic(self,pred,y,X):
    llf = self.__calc_llf(pred,y,X)
    nobs = float(len(X))
    k_params = len(X.iloc[0])
    bic = -2*llf + np.log(nobs) * k_params
    return round(bic)

  def __progress(self,value, max=100):
    return HTML("""
        <progress
            value='{value}'
            max='{max}',
            style='width: 100%'
        >
            {value}
        </progress>
    """.format(value=value, max=max))

  def __superRFE(self,method,n_cols_2_remove,n_Kfold_CV):
    print("\nStarting RFE...\n")
    # Define o total de atributos a serem removidos por rodada
    n_cols_2_remove = max([int(len(self.data.columns)*n_cols_2_remove),1])

    # Define X inicial como descritores
    X_train = self.data
    tot2display = len(list(X_train.columns))
    # Define variável alvo
    if self.__sqrt_transform:
      y_train = np.array(self.__calc_new_sqrt_redimension(self.target))
    elif self.__transform:
      y_train = np.array(self.__calc_new_redimension(self.target))
    else:
      y_train = self.target

    # Inicializa tabela de resultados
    resultTable = pd.DataFrame(columns=['Atributos','R² adj','F-statistic','BIC','MSE-CV'])
    percentagedisplay = round(100 - (len(list(X_train.columns))/tot2display)*100)
    out = display(self.__progress(0, 100), display_id=True)
    while len(X_train.columns) - n_cols_2_remove > n_cols_2_remove or len(X_train.columns) > 1:
      X = self.__toCLR(X_train)

      method.fit(X,y_train)

      pred = method.predict(X)

      Fprob = self.__calc_f_prob_centeredv2(pred,y_train,X)

      r2 = self.__calc_r_squared(pred,y_train)
      r2adj = self.__calc_rsquared_adj(X,r2)

      BIC = self.__calc_bic(pred,y_train,X)

      msecv_results = []
      #Adicionando etapa de validação cruzada
      kf = KFold(n_splits=n_Kfold_CV,shuffle=True,random_state=42)

      for train, test in kf.split(X):

        model = method.fit(X.iloc[train],y_train[train])

        predcv = model.predict(X.iloc[test])

        msecv_results.append(np.mean([(t-p)**2 for t,p in zip(y_train[test],predcv)])**(1/2))

      msecv = np.mean(msecv_results)

      # caso consiga calcular um p-valor
      if not math.isnan(Fprob) and r2adj < 1.0:
        # Cria linha com: Atributos separados por ';', R² ajustado, estatistica F e estatistica BIC
        newline = pd.DataFrame.from_records([{'Atributos':'@'.join(list(X.columns)),'R² adj':float(r2adj),'F-statistic':float(Fprob),'BIC':float(BIC),'MSE-CV':float(msecv)}])

        # Adiciona linha na tabela de resultado
        resultTable = pd.concat([resultTable,newline])

      # Cria tabela de dados dos atributos
      atr = pd.DataFrame(data = [[xx,w] for xx,w in zip(X.columns,method.coef_)],columns = ['Atributos','coef'])

      # Transforma coluna de coeficiente p/ float
      atr = atr.astype({'coef':float})

      # Remove colunas com coeficientes iguais ou menores que 0 / Acelera o rfe
      atr = atr[atr.coef != 0]# Remove zeros
      atr.coef = atr.coef.abs()#Transforma em abs para remover apenas os X% mais perto de zero

      # Ordena de forma decrescente pelo coeficiente
      atr = atr.sort_values(by=['coef'],ascending=False)

      # Cria lista de atributos selecionados
      atributos = list(atr.Atributos)

      # Remove espaços em brancos inseridos pela tabela de atributos
      atributos = [x.strip() for x in atributos]

      # Remove n_cols_2_remove menos relevantes
      atributos = atributos[:-n_cols_2_remove]

      # Remove atributos n selecionados
      X_train = X_train[atributos]

      # Calculo da % para mostrar na tela
      percentagedisplay = round(100 - (len(list(X_train.columns))/tot2display)*100)
      #print(percentagedisplay,'% done...\n')
      out.update(self.__progress(int(percentagedisplay), 100))
    #Remove possiveis nan
    resultTable.dropna(inplace=True)
    #print('100% done!\n')
    out.update(self.__progress(100, 100))
    # Retorna a tabela com os resultados
    return resultTable

  def __scoreAndSelection(self,resultTable,weightR2,weightProbF,weightBIC,weightRMSE):
    # Cria cópia da tabela original
    df_aux = resultTable.copy()
    df_aux.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_aux.dropna(inplace=True)

    # Normaliza o R² ajustado
    df_aux['R² adj'] = MinMaxScaler().fit_transform(np.array(df_aux['R² adj']).reshape(-1,1))

    # Aplica a transformação -log10(f) e então normaliza a estatistica f
    df_aux['F-statistic'] = [-math.log10(x) if x !=0 else sys.float_info.max for x in df_aux['F-statistic']]
    df_aux['F-statistic'] = MinMaxScaler().fit_transform(np.array(df_aux['F-statistic']).reshape(-1,1))

    # Normaliza e então inverte a estatistica BIC (Quanto menor menor)
    df_aux['BIC'] = MinMaxScaler().fit_transform(np.array(df_aux['BIC']).reshape(-1,1))
    df_aux['BIC'] = [np.clip(1-x,0,1) for x in df_aux['BIC']]

    # Normaliza 'MSE-CV' e inverte a estatistica MSE-cv
    df_aux['MSE-CV'] = MinMaxScaler().fit_transform(np.array(df_aux['MSE-CV']).reshape(-1,1))
    df_aux['MSE-CV'] = [np.clip(1-x,0,1) for x in df_aux['MSE-CV']]

    # Cria coluna de Score
    df_aux['Score'] = [(r*weightR2)+(f*weightProbF)+(b*weightBIC)+(m*weightRMSE) for r,f,b,m in zip(df_aux['R² adj'],df_aux['F-statistic'],df_aux['BIC'],df_aux['MSE-CV'])]

    # Encontra indice de maior Score
    indexSelected = list(df_aux.Score).index(max(list(df_aux.Score)))

    # Seleciona atributos
    selected = df_aux.iloc[indexSelected].Atributos.split('@')

    self.selected_taxa = selected # salva os atributos selecionados

    retEstatisticas = list(resultTable.iloc[indexSelected][['R² adj','F-statistic','BIC','MSE-CV']])

    self.results = {'R² adj':retEstatisticas[0],
                    'F-statistic':retEstatisticas[1],
                    'BIC':retEstatisticas[2],
                    'MSE-CV':retEstatisticas[3]} # Salva as estatisticas

    retScore = df_aux.iloc[indexSelected].Score

    self.score_best_model = retScore # Salva a pontuação do melhor modelo

  def __write_results(self,path_out,name_append):
    # adiciona '/' caso n tneha
    if path_out != '':
      if path_out[-1]!= '/':
        path_out+='/'
    else:
      path_out = '/'.join(self.__path2MetaData.split('/')[:-1])+'/'
    # adiciona '_' caso n tenha
    if name_append != '':
      if name_append[0]!= '_':
        name_append = 'CODARFE_RESULTS_'+name_append
    else:
      name_append = 'CODARFE_RESULTS'

    path2write = path_out +name_append+'.txt'
    print('Writing results at ',path2write)

    with open(path2write,'w') as f:
      f.write('Results: \n\n')
      f.write('R² adj -> '+     str(self.results['R² adj'])+'\n')
      f.write('F-statistic -> '+str(self.results['F-statistic'])+'\n')
      f.write('BIC -> '+        str(self.results['BIC'])+'\n')
      f.write('MSE-CV -> '+     str(self.results['MSE-CV'])+'\n')
      f.write('Total selected predictors -> '+str(len(self.selected_taxa))+'. This value corresponds to '+str((len(self.selected_taxa)/len(self.data.columns))*100)+'% of the total observed\n\n')
      f.write('Selected predictors: \n\n')
      f.write(','.join(self.selected_taxa))

  def __DefineModel(self,allow_transform_high_variation):

      self.__model = RandomForestRegressor(n_estimators = 160, criterion = 'poisson',random_state=42)
      X = self.data[self.selected_taxa]
      X = self.__toCLR(X)

      if allow_transform_high_variation and np.std(self.target)/np.mean(self.target)>0.2:# Caso varie muitas vezes a média (ruido)
        targetLogTransformed = self.__calc_new_sqrt_redimension(self.target) # Aplica transformação no alvo
        self.__model.fit(X,targetLogTransformed) # Treina com o alvo transformado
        self.__sqrt_transform = True # Define flag de transformação
        self.__transform = False
      else:
        if any(t < 0 for t in self.target):
          self.__transform = True
          targetTranformed = self.__calc_new_redimension(self.target)
          self.__model.fit(X,targetTranformed)
          self.__sqrt_transform = False
          print(f"The data was shifted {abs(self.__min_target_transformed)} + 1 units due to negative values not supported by poisson distribution.")

        else:
          self.__model.fit(X,self.target) # Treina um segundo modelo com o alvo como é
          self.__sqrt_transform = False # Define flag de transformação
          self.__transform = False


  def __check_boolean(self,value, name):
      if not isinstance(value, bool):
          raise ValueError(f"{name} must be a boolean.")

  def __check_string(self,value, name):
      if not isinstance(value, str):
          raise ValueError(f"{name} must be a string.")

  def __check_integer_range(self,value, name, min_value, max_value):
      if value < min_value or value > max_value:
          raise ValueError(f"{name} must be between {min_value} and {max_value}.")

  def __check_integer(self,value, name):
      if not isinstance(value, int):
          raise ValueError(f"{name} must be an integer.")

  def __check_non_negative_float(self,value, name):
      if not isinstance(value, float):
          raise ValueError(f"{name} must be a float.")
      elif value < 0:
          raise ValueError(f"{name} must be greater than or equal to 0.")

  def __checkModelParams(self,
                         write_results,
                         path_out,
                         name_append,
                         rLowVar,
                         applyAbunRel,
                         allow_transform_high_variation,
                         percentage_cols_2_remove,
                         n_Kfold_CV,
                         weightR2,
                         weightProbF,
                         weightBIC,
                         weightRMSE,
                         n_max_iter_huber):
      self.__check_boolean(write_results, "write_results")
      self.__check_boolean(rLowVar, "rLowVar")
      self.__check_boolean(applyAbunRel, "applyAbunRel")
      self.__check_boolean(allow_transform_high_variation, "allow_transform_high_variation")
      self.__check_string(path_out, "path_out")
      if write_results and path_out != '' and not os.path.exists(path_out):
          raise FileNotFoundError("The path out does not exist!")
      self.__check_string(name_append, "name_append")
      self.__check_integer(percentage_cols_2_remove, "percentage_cols_2_remove")
      self.__check_integer_range(percentage_cols_2_remove, "percentage_cols_2_remove", 1, 99)
      self.__check_integer(n_Kfold_CV, "n_Kfold_CV")
      self.__check_integer_range(n_Kfold_CV, "n_Kfold_CV", 2, 100)
      self.__check_integer(n_max_iter_huber, "n_max_iter_huber")
      self.__check_integer_range(n_max_iter_huber, "n_max_iter_huber", 2, 1000)
      self.__check_non_negative_float(weightR2, "weightR2")
      self.__check_non_negative_float(weightProbF, "weightProbF")
      self.__check_non_negative_float(weightBIC, "weightBIC")
      self.__check_non_negative_float(weightRMSE, "weightRMSE")


  def CreateModel(self,
                  write_results: bool =False,
                  path_out: str ='',
                  name_append: str ='',
                  rLowVar: bool =True,
                  applyAbunRel: bool = True,
                  allow_transform_high_variation = True,
                  percentage_cols_2_remove: int =1,
                  n_Kfold_CV: int=10,
                  weightR2: float =1.0,
                  weightProbF: float=0.5,
                  weightBIC: float=1.0,
                  weightRMSE: float=1.5,
                  n_max_iter_huber: int=100) -> None:
    """
    Parameters
    ----------
    write_results:  bool = False
                    Defines if the results will be written. The results include the selected predictors and the metrics for its selection.
    path_out: str = ""
                    Where to write the results
    name_append: str = ""
                    The name to append in the end of the file with the results
    rLowVar: bool = True
                    Flag to define if it is necessary to apply the removal of predictors with low variance. Set as False if less than 300 predictors.
    applyAbunRel: bool = True
                    Flag to define if it is necessary to apply the relative abundance transformation. Set as False if the data is already transformed
    allow_transform_high_variation: bool = True
                    Flag to allow the target transformation in case it has a high variance.
    percentage_cols_2_remove: int = 1
                    Percentage of the total predictors removed in each iteraction of the RFE. HIGH IMPACT in the final result and computational time.
    n_Kfold_CV: int = 10
                    Number of folds in the Cross-validation step for the RMSE calculation. HIGH IMPACT in the final result and computational time.
    weightR2: float = 1.0
                    Weight of the R² metric in the model’s final score
    weightProbF: float = 0.5
                    Weight of the Probability of the F-test metric in the model’s final score
    weightBIC: float = 1.0
                    Weight of the BIC metric in the model’s final score
    weightRMSE: float = 1.5
                    Weight of the RMSE metric in the model’s final score
    n_max_iter_huber: int = 100
                    Maximum number of iterations of the huber regression. HIGH IMPACT in the final result and computational time.

    Returns
    -------
    None

    Raises
    ------
    ValueError
                    If any of the parameters is not the correct type or is outside the range

    """


    if type(self.data) == type(None):
      print('No data was provided!\nPlease make sure to provide complete information or use the Load_Instance(<path_2_instance>) function to load an already created CODARFE model')
      return None
    print('\n\nChecking model parameters...',end="")
    self.__checkModelParams(write_results,path_out,name_append,rLowVar,applyAbunRel,allow_transform_high_variation,percentage_cols_2_remove,n_Kfold_CV,weightR2,weightProbF,weightBIC,weightRMSE,n_max_iter_huber)
    print('OK')

    n_cols_2_remove = percentage_cols_2_remove/100
    self.__n_max_iter_huber = n_max_iter_huber # Define o numero de iterações utilziado pelo huber

    if rLowVar:
      #Remove baixa variância
      self.__removeLowVar()

    if applyAbunRel:
      #transforma em abundância relativa
      self.data = self.__toAbunRel(self.data)

    method = HuberRegressor(epsilon = 2.0,alpha = 0.0003, max_iter = n_max_iter_huber)

    # Remove iterativamente atributos enquanto cria vários modelos
    resultTable = self.__superRFE(method,n_cols_2_remove,n_Kfold_CV)

    if len(resultTable)>0:
      
    
      # Calcula pontuação e seleciona o melhor modelo
      self.__scoreAndSelection(resultTable,weightR2,weightProbF,weightBIC,weightRMSE)

      self.__DefineModel(allow_transform_high_variation)

      print('\nModel created!\n\n')
      print('Results: \n\n')
      print('R² adj -> ',     self.results['R² adj'])
      print('F-statistic -> ',self.results['F-statistic'])
      print('BIC -> ',        self.results['BIC'])
      print('MSE-CV -> ',     self.results['MSE-CV'])
      print('Total selected predictors -> ',len(self.selected_taxa),'. This value corresponds to ',(len(self.selected_taxa)/self.__totalPredictorsInDatabase)*100,'% of the total observed.\n')

      if write_results:
        self.__write_results(path_out,name_append)

      if float(self.results['R² adj']) <= 0 or float(self.results['R² adj'])>1.0:
        warnings.warn("The model created has poor generalization power, please check codarfe.results before using it for prediction.",LowFitModelWarning)

      if float(self.results['F-statistic']) > 0.5:
        warnings.warn("The model has a p-value not statistically significant for the selected features! Please consider check your data and re-run the model-training.",NotSignificantPvalueWarning)

    else:
      warnings.warn('The model was not able to generalize your Data. Consider checking your data and re-run the model-training.',ImpossibleToGeneralizeWarning)

  def __pairwise_correlation(self,A, B):
    am = A - np.mean(A, axis=0, keepdims=True)
    bm = B - np.mean(B, axis=0, keepdims=True)
    return am.T @ bm /  (np.sqrt(
        np.sum(am**2, axis=0,
               keepdims=True)).T * np.sqrt(
        np.sum(bm**2, axis=0, keepdims=True)))

  def __CreateCorrelationImputer(self):
    threshold = 0.6 # Considered as strong correlation
    aux = self.__toCLR(self.data) # Remove composicionalidade usando CLR nos dados originais

    for selected in self.selected_taxa: # Para cada taxa selecionada
      self.__correlation_list[selected] = [] # Cria instancia para esta taxa selecionada
      for taxa in aux.columns: # Verifica correlação com todas as outras
        if taxa != selected: # n comparar consigo mesmo
          corr = self.__pairwise_correlation(np.array(aux[selected]),np.array(aux[taxa]))# Calcula a correlação de forma rapida
          if corr >= threshold: # Somenta adiciona caso seja fortemente correlacionada
            self.__correlation_list[selected].append({'taxa':taxa,'corr':corr}) # Adiciona taxa correlacionada
      self.__correlation_list[selected].sort(reverse=True,key = lambda x: x['corr']) # Ordena pela correlação

  def __Read_new_Data(self,path2Data):
    extension = path2Data.split('.')[-1]
    if extension == 'csv':
        data = pd.read_csv(path2Data,encoding='latin1')
        data.set_index(list(data.columns)[0],inplace=True)
    elif extension == 'tsv':
        data = pd.read_csv(path2Data,sep='\t',encoding='latin1')
        data.set_index(list(data.columns)[0],inplace=True)
    elif extension == 'biom':
        table = load_table(path2Data)
        data = table.to_dataframe()
    elif extension == 'qza':
        output_directory =  '/'.join(path2Data.split('/')[:-1])+'/QZA_EXTRACT_CODARFE_TEMP/'
        # Openning the .qza file as an zip file
        with zipfile.ZipFile(path2Data, 'r') as zip_ref:
            # extracting all data to the output directory
            zip_ref.extractall(output_directory)
        # Getting the biom path file
        biompath = output_directory+os.listdir(output_directory)[0]+'/data/'
        biompath += [f for f in os.listdir(biompath) if f[-5:]=='.biom'][0]
        table = load_table(biompath)# Read the biom file
        data = table.to_dataframe() # Tranform it to a pandas dataframe

        shutil.rmtree(output_directory) # remove the pathTree created
    return data

  def Predict(self,
              new: pd.DataFrame,
              applyAbunRel: bool = True,
              writeResults: bool = False,
              path_out: str = '',
              name_append: str = ''
              ) -> Optional[Tuple[pd.DataFrame,int]]:
    """
    Parameters
    ---------
    new : pd.Dataframe
          The dataframe with new samples for predicting the target variable
    applyAbunRel: bool = True
          Flag to apply relative abundance transformation
    writeResults: bool = False
          Flag to write the results
    path_out: str = ""
          Filename of the output. If no filename is provided it will be saved in the same directory as the metadata with the name of 'Prediction.csv'
    name_append: str = ""
          Name to concatenate in the final filename. (Use it to differentiate predictions from the same model)

    Returns
    -------
      Tuple with a Pandas Dataframe and a integer
        Pandas Dataframe: Two columns: index and predicts
        Integer : The number of predictors that were missing from the new samples (higher the number, higher the error chance; refer to the original paper)

      If the new data contains fewer than 25% of the total predictors, no prediction is made and None is returned.

    Raises
    -------
      ModelNotCreatedError:
        If the model was not created yet
      FileNotFoundError:
        If writeResults is True but there is no path_out or path_out does not exists
    """
    if self.__model == None:
      raise self.ModelNotCreatedError()

    if writeResults and ((path_out != '' and not os.path.exists(path_out)) or path_out == ''):
      raise FileNotFoundError('\nThe path out does not exists or is empty.')

    #new = self.__Read_new_Data(path2newdata)
    newindex = new.index

    if self.__correlation_list == {}:
      print('\n\nCreating correlation list for imputation method. It may take a few minutes depending on the size of the original dataset, but it will be create only once.\n\n')
      self.__CreateCorrelationImputer()
      print('Correlation list created!\n\n')

    data2predict = pd.DataFrame() # Cria um dataframe para colocar apenas os dados selecionados
    totalNotFound = 0
    for selected in self.selected_taxa: # Para cada taxa selecionada
      if selected in new.columns: # Caso exista no novo conjunto
        data2predict[selected] = new[selected] # Adiciona o valor do novo conjunto no df de previsão
      else: # Senão
        found = False # Flag que indica se encontrou substitudo
        for correlated_2_selected in self.__correlation_list[selected]: # Para cada taxa correlacionada com a que não existe
          if correlated_2_selected['taxa'] in new.columns: # Caso encontre um substituto
            data2predict[selected] = new[correlated_2_selected['taxa']] # Coloca ele no lugar do que n existe
            found = True # Seta flag
            break
        if not found:
          data2predict[selected] = 0 # Caso não encontra retorna zero
          print('Warning! Taxa ',selected,' was not found and have no correlations! It may affect the model accuracy')
          totalNotFound+=1

    if totalNotFound >= len(self.selected_taxa)*0.75:
      warnings.warn('The new samples has less than 25% of selected taxa. The model will not be able to predict it.')
      return None,totalNotFound


    data2predict = data2predict.fillna(0)

    if applyAbunRel:
      data2predict = self.__toAbunRel(data2predict) # Transforma em abundancia relativa

    data2predict = self.__toCLR(data2predict) # Transforma para CLR

    resp = self.__model.predict(data2predict)

    if self.__sqrt_transform: # Caso o modelo tenha sido treinado nos dados log transformados
      resp = self.__calc_inverse_sqrt_redimension(resp)#,totalNotFound # Retorna os valores restaurados ao original
    if self.__transform:
      resp = self.__calc_inverse_redimension(resp) # Retorna os valores restaurados ao original

    if writeResults:

      if path_out != '':
        if path_out[-1]!= '/':
          path_out+='/Prediction'

      if name_append != '':
        name_append = '_'+name_append
      filename = path_out+name_append+'.csv'
      pd.DataFrame(data = resp,columns = ['Prediction'],index=newindex).to_csv(filename)

    return resp,totalNotFound

  def Plot_Correlation(self,saveImg: bool=False,path_out: str='',name_append: str='') -> None:
    """
    Parameters
    ---------
    saveImg:  bool = False
              Flag that defines if the img will be saved
    path_out: str = ""
              The path to the folder where the img will be saved
    name_append: str = ""
              The name to append in the end of the img name (Correlation_<name_append>)
    
    Returns
    ------
    None

    Raises
    ------
    ModelNotCreatedError:
              if the CODARFE.CreateModel was not run yet
    FileNotFoundError:
              If the path_out does not exists
    """
    if self.__model == None:
      raise self.ModelNotCreatedError()

    if path_out != '' and not os.path.exists(path_out):
      raise FileNotFoundError("\nThe path out does not exists.\nPlease try again with the correct path or let it blank to write in the same path as the metadata")

    # Build a rectangle in axes coords
    left, width = .15, .75
    bottom, height = .15, .75
    right = left + width
    top = bottom + height
    y = self.target
    X = self.data[self.selected_taxa]
    X = self.__toCLR(X)
    pred = self.__model.predict(X)

    if self.__sqrt_transform: # Caso tenha aprendido com valores transformados
      pred = self.__calc_inverse_redimension(pred) # Destransforma-os
    plt.figure()
    plt.clf()
    ax = plt.gca()

    corr, what = pearsonr(y, pred)

    #Plota os pontos previsto por esperado
    plt.plot(pred, y, 'o')

    # calcula o slop e intercept para uma regressão linear (plot da linha)
    m, b = np.polyfit(pred, y, 1)

    #Adiciona a linha no plot
    plt.plot(pred, m*pred+b)
    shiftX = 0.2 * max(pred)
    shiftY = 0.1 * max(y)

    ax.text(left, top, 'R = '+str(round(corr,2))+', p < '+str(round(what,2)),
          horizontalalignment='center',
          verticalalignment='center',
          transform=ax.transAxes)

    if saveImg:
      if path_out != '':
        if path_out[-1]!= '/':
          path_out+='/'

        # adiciona '_' caso n tenha
        if name_append != '':
          if name_append[0]!= '_':
            name_append = 'Correlation_'+name_append
          else:
            name_append = 'Correlation'
        filename = path_out+name_append+'.png'

        print('\nSaving the image in ',filename)
        plt.savefig(filename, dpi=600, bbox_inches='tight')

      else:
        print("Please, provide an output path.")

    plt.show()

  def __checkHoldOutParams(self,n_repetitions,test_size,path_out,name_append):
    self.__check_integer(n_repetitions,"n_repetitions")
    self.__check_integer_range(n_repetitions,"n_repetitions",2,1000)
    self.__check_integer(test_size,"test_size")
    self.__check_integer_range(test_size,"test_size",1,99)
    if path_out != '' and not os.path.exists(path_out):
      raise FileNotFoundError("\nThe path out does not exists.\nPlease try again with the correct path or let it blank to write in the same path as the metadata")


  def Plot_HoldOut_Validation(self,
                              n_repetitions: int = 100,
                              test_size: int = 20,
                              saveImg: str = False,
                              path_out: str = '',
                              name_append: str = '') -> None:

    """
    Parameters
    ---------
    n_repetitions:  int = 100
                    Defines the number of repetitions (dots in the plot)
    test_size: int = 20
                    Defines the size of the hold-out samples
    saveImg:  bool = False
              Flag that defines if the img will be saved
    path_out: str = ""
              The path to the folder where the img will be saved
    name_append: str = ""
              The name to append in the end of the img name (HoldOut_Validation_<name_append>)

    Returns
    -------
    None

    Raises
    ------
    ValueError
              If any of the parameters is not the correct type or is outside the range
    ModelNotCreatedError
              if the CODARFE.CreateModel was not run yet
    FileNotFoundError:
              If the path_out does not exists
    """
    if self.__model == None:
      raise self.ModelNotCreatedError()

    self.__checkHoldOutParams(n_repetitions,test_size,path_out,name_append)


    test_size = test_size/100
    method = RandomForestRegressor(n_estimators = 160, criterion = 'poisson',random_state=42)
    X = self.data[self.selected_taxa]
    X = self.__toCLR(X)
    y = self.target
    maes = []
    out = display(self.__progress(0, 100), display_id=True)
    for i in range(n_repetitions):
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size) # divide em treino e teste

      if self.__sqrt_transform: # Caso tenha aprendido originalmente com valores transformados
        method.fit(X_train,self.__calc_new_redimension(y_train)) # Re-treina com os valores transformados
        y_pred = method.predict(X_test) # Realiza a predição
        y_pred = self.__calc_inverse_redimension(y_pred) # Destransforma-os
      else:
        method.fit(X_train,y_train)
        y_pred = method.predict(X_test)

      # Calculo do MAE
      tt = 0
      for ii in range(len(y_pred)):
        tt+=abs(y_test.iloc[ii]-y_pred[ii])
      maes.append(tt/len(y_pred))
      out.update(self.__progress(int((i/n_repetitions)*100), 100))

    sns.set_theme(style="ticks")

    out.update(self.__progress(100, 100))
    # Cria a figura zerada
    plt.figure()
    f, ax = plt.subplots(figsize=(7, 6))

    # Plota o boxplot
    sns.boxplot(x=[1]*len(maes),
                y=maes,
                whis=[0, 100],
                width=.6,
                palette="vlag")

    # Adiciona os pontos sobre o boxplot
    sns.stripplot(x=[1]*len(maes),
                  y=maes,
                  size=4,
                  color=".3",
                  linewidth=0)

    # Tweak the visual presentation
    ax.xaxis.grid(True)
    ax.set(ylabel="")
    sns.despine(trim=True, left=True)

    trainSize = int((1-test_size) *100)
    testSize = int(test_size*100)
    ax.set_title('Hold-out Validation ('+str(trainSize)+'-'+str(testSize)+') '+str(n_repetitions)+' repetitions',fontweight='bold')
    ax.set_ylabel('Mean Absolute Error')
    #ax.set_xlabel(target+' MAE')

    if saveImg:
      if path_out != '':
        if path_out[-1]!= '/':
          path_out+='/'

        # adiciona '_' caso n tenha
        if name_append != '':
          if name_append[0]!= '_':
            name_append = 'HoldOut_Validation_'+name_append
          else:
            name_append = 'HoldOut_Validation'
        filename = path_out+name_append+'.png'

        print('\nSaving the image in ',filename)
        plt.savefig(filename, dpi=600, bbox_inches='tight')

      else:
        print("Please, provide an output path.")

    plt.show()


  def Plot_Relevant_Predictors(self,
                               n_max_features: int = 100,
                               saveImg: bool = False,
                               path_out: str = '',
                               name_append: str = '') -> None:
    """
    Parameters
    ---------
    n_max_features:  int = 100
                    Defines the maximum number of features/predictors to be displayed (bars in the plot)
    saveImg:  bool = False
              Flag that defines if the img will be saved
    path_out: str = ""
              The path to the folder where the img will be saved
    name_append: str = ""
              The name to append in the end of the img name (HoldOut_Validation_<name_append>)

    Returns
    -------
    None

    Raises
    ------
    ValueError
              If any of the parameters is not the correct type or is outside the range
    ModelNotCreatedError
              if the CODARFE.CreateModel was not run yet
    FileNotFoundError:
              If the path_out does not exists
    """

    if self.__model == None:
      raise self.ModelNotCreatedError()
    self.__check_integer(n_max_features,"n_max_features")
    self.__check_integer_range(n_max_features,"n_max_features",2,1000)

    if path_out != '' and not os.path.exists(path_out):
      raise FileNotFoundError("\nThe path out does not exists.\nPlease try again with the correct path or let it blank to write in the same path as the metadata")

    method = HuberRegressor(epsilon = 2.0,alpha = 0.0003, max_iter = self.__n_max_iter_huber)
    X = self.data[self.selected_taxa]
    X = self.__toCLR(X)
    y = self.target
    resp = method.fit(X,y)

    dfaux = pd.DataFrame(data={'features':resp.feature_names_in_,'coefs':resp.coef_})
    dfaux.sort_values(by='coefs',ascending=False,inplace=True,ignore_index=True)

    if len(dfaux) > n_max_features:
      half = int(n_max_features/2)
      totpos = len(dfaux.coefs[dfaux.coefs>0])
      totneg = len(dfaux.coefs[dfaux.coefs<0])

      if totpos < half:
        totneg = half+half-totpos
      elif totneg < half:
        totpos = half+half-totneg
      else:
        totpos = half
        totneg = half

      dfaux = dfaux[dfaux.index.isin([i for i in range(0,totpos)] + [i for i in range(len(dfaux)-totneg,len(dfaux))])]
    plt.figure()
    sns.set_theme(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 15))#figsize=(6, 15)

    colors = ['b' if x > 0 else 'r' for x in dfaux.coefs]
    # Plot the total crashes
    sns.set_color_codes("pastel")
    sns.barplot(x="coefs",
                y="features",
                data=dfaux,
                palette=colors,
                )

    ax.set_title('Strength of relevant predictors',fontweight='bold')
    ax.set(ylabel="Predictor name",
          xlabel="Coefficient weight")
    sns.despine(left=True, bottom=True)

    if saveImg:
      if path_out != '':
        if path_out[-1]!= '/':
          path_out+='/'

        # adiciona '_' caso n tenha
        if name_append != '':
          if name_append[0]!= '_':
            name_append = 'Relevant_Predictors_'+name_append
          else:
            name_append = 'Relevant_Predictors'
        filename = path_out+name_append+'.png'

        print('\nSaving the image in ',filename)
        plt.savefig(filename, dpi=600, bbox_inches='tight')

      else:
        print("Please, provide an output path.")

    plt.show()

  # The next 2 functions I got from the skbio github. So it is not necessary to install the whole library.

  def __svd_rank(self,M_shape, S, tol=None):
    """Matrix rank of `M` given its singular values `S`.

    See `np.linalg.matrix_rank` for a rationale on the tolerance
    (we're not using that function because it doesn't let us reuse a
    precomputed SVD)."""
    if tol is None:
        tol = S.max() * max(M_shape) * np.finfo(S.dtype).eps
    return np.sum(S > tol)

  def __ca(self,X, scaling=1):
    r"""Compute correspondence analysis, a multivariate statistical
    technique for ordination.

    In general, rows in the data table will correspond to samples and
    columns to features, but the method is symmetric. In order to
    measure the correspondence between rows and columns, the
    :math:`\chi^2` distance is used, and those distances are preserved
    in the transformed space. The :math:`\chi^2` distance doesn't take
    double zeros into account, and so it is expected to produce better
    ordination that PCA when the data has lots of zero values.

    It is related to Principal Component Analysis (PCA) but it should
    be preferred in the case of steep or long gradients, that is, when
    there are many zeros in the input data matrix.

    Parameters
    ----------
    X : pd.DataFrame
        Samples by features table (n, m). It can be applied to different kinds
        of data tables but data must be non-negative and dimensionally
        homogeneous (quantitative or binary). The rows correspond to the
        samples and the columns correspond to the features.
    scaling : {1, 2}
        For a more detailed explanation of the interpretation, check Legendre &
        Legendre 1998, section 9.4.3. The notes that follow are quick
        recommendations.

        Scaling type 1 maintains :math:`\chi^2` distances between rows
        (samples): in the transformed space, the euclidean distances between
        rows are equal to the :math:`\chi^2` distances between rows in the
        original space. It should be used when studying the ordination of
        samples. Rows (samples) that are near a column (features) have high
        contributions from it.

        Scaling type 2 preserves :math:`\chi^2` distances between columns
        (features), so euclidean distance between columns after transformation
        is equal to :math:`\chi^2` distance between columns in the original
        space. It is best used when we are interested in the ordination of
        features. A column (features) that is next to a row (sample) means that
        it is more abundant there.

        Other types of scalings are currently not implemented, as they're less
        used by ecologists (Legendre & Legendre 1998, p. 456).

        In general, features appearing far from the center of the biplot and
        far from its edges will probably exhibit better relationships than
        features either in the center (may be multimodal features, not related
        to the shown ordination axes...) or the edges (sparse features...).

    Returns
    -------
    OrdinationResults
        Object that stores the computed eigenvalues, the transformed sample
        coordinates, the transformed features coordinates and the proportion
        explained.

    Raises
    ------
    NotImplementedError
        If the scaling value is not either `1` or `2`.
    ValueError
        If any of the input matrix elements are negative.

    See Also
    --------
    cca
    rda
    OrdinationResults

    Notes
    -----
    The algorithm is based on [1]_, \S 9.4.1., and is expected to give the same
    results as ``cca(X)`` in R's package vegan.

    References
    ----------
    .. [1] Legendre P. and Legendre L. 1998. Numerical Ecology. Elsevier,
       Amsterdam.

    """

    if scaling not in {1, 2}:
        raise NotImplementedError(
            "Scaling {0} not implemented.".format(scaling))

    short_method_name = 'CA'
    long_method_name = 'Correspondance Analysis'

    # we deconstruct the dataframe to avoid duplicating the data and be able
    # to perform operations on the matrix
    row_ids = X.index
    column_ids = X.columns
    X = np.asarray(X.values, dtype=np.float64)

    # Correspondance Analysis
    r, c = X.shape

    if X.min() < 0:
        raise ValueError("Input matrix elements must be non-negative.")

    # Step 1 (similar to Pearson chi-square statistic)
    grand_total = X.sum()
    Q = X / grand_total

    column_marginals = Q.sum(axis=0)
    row_marginals = Q.sum(axis=1)

    # Formula 9.32 in Lagrange & Lagrange (1998). Notice that it's
    # an scaled version of the contribution of each cell towards
    # Pearson chi-square statistic.
    expected = np.outer(row_marginals, column_marginals)
    Q_bar = (Q - expected) / np.sqrt(expected)  # Eq. 9.32

    # Step 2 (Singular Value Decomposition)
    U_hat, W, Ut = svd(Q_bar, full_matrices=False)
    # Due to the centering, there are at most min(r, c) - 1 non-zero
    # eigenvalues (which are all positive)
    rank = self.__svd_rank(Q_bar.shape, W)
    assert rank <= min(r, c) - 1
    U_hat = U_hat[:, :rank]
    W = W[:rank]
    U = Ut[:rank].T

    # Both scalings are a bit intertwined, so we'll compute both and
    # then choose
    V = column_marginals[:, None]**-0.5 * U
    V_hat = row_marginals[:, None]**-0.5 * U_hat
    F = V_hat * W

    F_hat = V * W

    # Eigenvalues
    eigvals = W**2

    # features scores
    features_scores = [V, F_hat][scaling - 1]
    # sample scores (weighted averages of features scores)
    sample_scores = [F, V_hat][scaling - 1]

    # build the OrdinationResults object
    sample_columns = ['%s%d' % (short_method_name, i+1)
                      for i in range(sample_scores.shape[1])]
    feature_columns = ['%s%d' % (short_method_name, i+1)
                       for i in range(features_scores.shape[1])]

    eigvals = pd.Series(eigvals, ['%s%d' % (short_method_name, i+1) for i in
                                  range(eigvals.shape[0])])
    samples = pd.DataFrame(sample_scores, row_ids, sample_columns)
    features = pd.DataFrame(features_scores, column_ids, feature_columns)

    return features


  # HEAT MAP (ps: eu n lembro de porra nenhuma de como eu criei isso... melhor n tentar otimizar nada)
  def __neatMapLinkage(self,selected_features):
    # Correcting for bad user inputation
    selected_features = selected_features.fillna(0)
    selected_features = selected_features.replace([np.inf, -np.inf], 0)

    selected_features+=0.001

    w = self.__ca(selected_features)

    pc1 = w['CA1']
    pc2 = w['CA2']

    # w = ca(selected_features)
    # pc1 = w.features['CA1']
    # pc2 = w.features['CA2']

    xc = np.mean(pc1)
    yc = np.mean(pc2)
    theta = []
    for i in range(len(pc1)):
      theta.append(math.atan2(pc2[i] - yc, pc1[i] - xc ))
    order = [index for index, element in sorted(enumerate(theta), key=operator.itemgetter(1))]
    names = [selected_features.columns[i] for i in order]
    return names

  def __heatmap(self,data, row_labels, col_labels, ax=None,cbar_kw={}, cbarlabel="", **kwargs):

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    cbar = ax.figure.colorbar(im, ax=ax,cax=cax, **cbar_kw)#im
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticklabels(labels=col_labels)
    ax.set_yticklabels(labels=row_labels)
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                    labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-90, ha="right",
              rotation_mode="anchor")

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar

  def Plot_Heatmap(self,
                   saveImg: bool=False,
                   path_out: str='',
                   name_append: str=''
                   ) -> None:
    """
    Parameters
    ---------
    saveImg:  bool = False
              Flag that defines if the img will be saved
    path_out: str = ""
              The path to the folder where the img will be saved
    name_append: str = ""
              The name to append in the end of the img name (HeatMap_<name_append>)

    Returns
    -------
    None

    Raises
    ------
    ModelNotCreatedError
              if the CODARFE.CreateModel was not run yet
    FileNotFoundError:
              If the path_out does not exists
    """

    if self.__model == None:
      raise self.ModelNotCreatedError()

    if path_out != '' and not os.path.exists(path_out):
      raise FileNotFoundError("\nThe path out does not exists.\nPlease try again with the correct path or let it blank to write in the same path as the metadata")

    # Pega o dataframe original porem apenas o que foi selecioando
    selected_features = self.data[self.selected_taxa]

    # Clusterizando bacterias
    y = self.target

    ###### Aqui clusteriza por CA ############
    leaf_names = self.__neatMapLinkage(selected_features)
    ##########################################
    clustered_df = pd.DataFrame()

    for name in leaf_names:
      clustered_df[name] = selected_features[name]
    clustered_df['Target'] = y
    selected_features = clustered_df

    # Ordenando bacterias por variável alvo
    selected_features_t = selected_features.T
    sorted_t = selected_features_t.sort_values(by='Target',axis=1,ascending=False)
    y = list(sorted_t.iloc[-1])

    # Separando os dados para o plot
    bac_counts = sorted_t.drop('Target',axis=0).replace(0,0.5).values

    bacs = list(sorted_t.drop('Target',axis=0).index[:])

    # Aplica o CLR
    bac_clr = self.__toCLR(pd.DataFrame(data=bac_counts))#bac_clr = clr(bac_counts+0.001)
    vmin = min(bac_clr.values.flatten())
    vmax = max(bac_clr.values.flatten())
    norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

    Largura = int(len(y)*0.2)
    Altura  = int(len(bac_counts)*0.2)
    if Largura < 15:
      Largura = 15
    if Altura < 20:
      Altura = 20
    if Largura > 150:
      Largura = 150
    if Altura > 200:
      Altura = 200
    plt.figure()
    fig, ax = plt.subplots(figsize=(Largura,Altura))

    im, cbar = self.__heatmap(bac_clr, bacs, y, ax=ax, cmap="RdYlBu",norm = norm, cbarlabel="Center-Log-Ratio")

    #fig.tight_layout()
    if saveImg:
      if path_out != '':
        if path_out[-1]!= '/':
          path_out+='/'

        # adiciona '_' caso n tenha
        if name_append != '':
          if name_append[0]!= '_':
            name_append = 'HeatMap_'+name_append
          else:
            name_append = 'HeatMap'
        filename = path_out+name_append+'.png'

        print('\nSaving the image in ',filename)
        plt.savefig(filename, dpi=600, bbox_inches='tight')

      else:
        print("Please, provide an output path.")

    plt.show()