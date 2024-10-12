# Ataskaita

## Algoritmo analizė

### Pirma dalis

| numDP | numCL |
| :---: | :---: |
| 5000  |  50   |

|     | Matricos skaičiavimas | sprendimo paieškos |
| --- | --------------------- | ------------------ |
| 1   | 4.45                  | 15.04              |
| 2   | 4.47                  | 15.15              |
| 3   | 4.51                  | 15.39              |
| Avg | 4.47                  | 15.19              |

## Antra dalis

$$\alpha\approx\frac{4.47}{4.47 + 15.19}\approx 0.22$$
$$\beta\approx\frac{15.19}{4.47 + 15.19}\approx 0.78$$
$$\tilde{S}_2=\frac{1}{\alpha+\frac{\beta}{2}}\approx 1.64$$
$$\tilde{S}_4=\frac{1}{\alpha+\frac{\beta}{4}}\approx 2.40$$
$$\tilde{S}_{max}=\lim_{p\to\infty}\frac{1}{\alpha+\frac{\beta}{p}}=\frac{1}{\alpha}\approx 4.54$$