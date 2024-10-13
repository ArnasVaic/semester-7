# Ataskaita

## Algoritmo analizė

### Parametrų parinktis

| numDP | numCL |
| :---: | :---: |
| 5000  |  50   |

|     | Matricos skaičiavimas | sprendimo paieškos |
| --- | --------------------- | ------------------ |
| 1   | 4.45                  | 15.04              |
| 2   | 4.47                  | 15.15              |
| 3   | 4.51                  | 15.39              |

### Teorinio pagreitėjimo vertinimas

$$\alpha\approx\frac{4.47}{4.47 + 15.19}\approx 0.22$$
$$\beta\approx\frac{15.19}{4.47 + 15.19}\approx 0.78$$
$$\tilde{S}_2=\frac{1}{\alpha+\frac{\beta}{2}}\approx 1.64$$
$$\tilde{S}_4=\frac{1}{\alpha+\frac{\beta}{4}}\approx 2.40$$
$$\tilde{S}_{max}=\lim_{p\to\infty}\frac{1}{\alpha+\frac{\beta}{p}}=\frac{1}{\alpha}\approx 4.54$$

## Bendros atminties lygiagrečiojo algoritmo sudarymas

## Pirma dalis

Nuoseklioji dalis - duomenų įkėlimas ir atstumų matricos skaičiavimas.
Lygiagretinama dalis - sprendinių perrinkimas.

### Eksperimento duomenys

Duomenys gauti su dvejais procesoriais ($p=2$)

|     | Matricos skaičiavimas | sprendimo paieškos |
| --- | --------------------- | ------------------ |
| 1   | 4.43                  | 8.47               |
| 2   | 4.48                  | 8.81               |
| 3   | 4.69                  | 8.31               |

Duomenys gauti su keturiais procesoriais ($p=4$)

|     | Matricos skaičiavimas | sprendimo paieškos |
| --- | --------------------- | ------------------ |
| 1   | 4.45                  | 4.16               |
| 2   | 4.55                  | 4.16               |
| 3   | 4.46                  | 4.24               |
