/** Original deterministic teaching example. Probabilities are constructed, not study estimates. */
export const STRATA = Object.freeze([
  Object.freeze({label:'低基线风险层', q0:0.12, q1:0.08}),
  Object.freeze({label:'高基线风险层', q0:0.36, q1:0.26})
]);
export function standardize(highWeight, treatedHigh=0.8, untreatedHigh=0.2) {
  for (const value of [highWeight,treatedHigh,untreatedHigh]) {
    if (!Number.isFinite(value) || value < 0 || value > 1) throw new RangeError('Weights must be within [0, 1]');
  }
  const mix=(key,p)=>STRATA[0][key]*(1-p)+STRATA[1][key]*p;
  const mu0=mix('q0',highWeight), mu1=mix('q1',highWeight);
  const crude0=mix('q0',untreatedHigh), crude1=mix('q1',treatedHigh);
  return {mu0,mu1,rd:mu1-mu0,rr:mu1/mu0,crude0,crude1,crudeRd:crude1-crude0};
}
export function percent(n,digits=1){return `${(n*100).toFixed(digits)}%`;}
export function points(n,digits=1){return `${n>0?'+':''}${(n*100).toFixed(digits)}`;}
