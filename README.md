# Gestion De Portefeuille sur Python

https://gestiondeportefeuille.streamlit.app

## Calcul pour une action:

### Rentabilité
ri = (Vi - Vi-1)/Vi-1

### Rentabilité moyenne
R = 1/n Σ (ri) 

### Variance
s² = Σ (ri - R)² / n-1

### Risque
s = √s²


## Calcul pour un portefeuille: 

### Rentabilité 
Rp = w1R1 + w2R2 + ... + wnRn

### Risque
COV(x,y) = (x - x̄) * (y - ȳ) / n-1

corr(x,y) = COV(x,y) / s(x) * s(y)

(w1s1 + w2s2)² = w1²s²1 + 2w1s1w2s2corr(1,2) + w2²s²2

