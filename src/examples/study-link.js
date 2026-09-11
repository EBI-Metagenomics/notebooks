// The URL contains data only; never interpolate it into executable Python or R.
export function readStudyAccession(search) {
  const params = new URLSearchParams(search);
  const study = (params.get("study") ?? params.get("jlvar_MGYS") ?? "MGYS00010393")
    .trim().toUpperCase();
  if (!/^MGYS[0-9]{8}$/.test(study)) {
    throw new Error("Invalid study accession. Use MGYS followed by eight digits, e.g. ?study=MGYS00010393.");
  }
  return study;
}
