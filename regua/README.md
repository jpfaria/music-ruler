# Régua de escalas — trilho + régua + cortinas

Mesma lógica da roda: uma camada fixa com toda a informação, camadas móveis que recortam.

## Imprimir
| Peça | Tamanho | Peso | Quantidade |
|---|---|---|---|
| `regua_1-TRILHO.stl` | 280 × 108 × 7,2 mm | ~54 g | 1 |
| `regua_2-REGUA-DESLIZANTE.stl` | 154 × 95 × 2,4 mm | ~12 g | 1 |
| `regua_3-CORTINA.stl` | 112 × 96 × 1,8 mm | ~8 g | **2** |

Sem suporte em nenhuma peça. Bico 0,4 · camada 0,16 · 3 perímetros · 20 %. **PETG.**
O trilho tem 280 mm — use **brim de 5 mm**, mesa a 80 °C e a câmara fechada, senão as
pontas levantam.

`arte-trilho.pdf` — **A4 DEITADO**, 100 % / tamanho real. Página 1 traz os dois painéis,
página 2 a legenda. Recorte um dos dois retângulos (o outro é reserva) e cole no rebaixo
do trilho.

### Montagem
Cole a **etiqueta das formas** no rebaixo do topo da régua antes de montar (página 2 do
PDF). O trilho tem **dois canais empilhados**, cada um com perfil de rabo de andorinha:

1. **canal de baixo** — entram as duas cortinas, deslizando por uma das pontas
2. **canal de cima** — entra a régua, do mesmo jeito

Nenhuma peça sai por cima: o canal fecha em 45° e a chapa é mais larga na base que na
boca. Nada de aba pendurada — foi justamente isso que saiu ruim na versão anterior,
porque era uma ponte de 1,5 mm impressa no ar.

## Como funciona
O trilho traz o **mapa de notas de 24 casas**. A régua tem furos nas notas da escala. Você desliza até a tônica cair no furo certo — e as 5 formas se posicionam sozinhas.

**Quadrado = tônica MAIOR. Losango = tônica MENOR relativa.**

- Alinhe um **quadrado** sobre o G → escala de G maior.
- Alinhe um **losango** sobre o E → escala de E menor.

### Em que tom eu estou — janela TOM
No canto superior esquerdo da régua tem uma **janela marcada TOM**. O papel do trilho traz
uma faixa de tonalidades no topo, e a janela emoldura exatamente uma delas: você lê
`C` em cima e `Am` embaixo, e pronto — é a tonalidade maior e a relativa menor daquela posição.
Não precisa contar nada.

Deslizando a régua uma casa pra direita a janela vira `C#` / `A#m`, e assim por diante.
As 12 posições úteis são as casas 1 a 12; da 13 em diante repete uma oitava acima.

### Onde cada forma começa e termina
No topo da régua tem uma **tabela de 5 caixas**. Cada caixa é uma forma: onde a caixa
começa a forma começa, onde ela acaba a forma acaba. Número **de cima = tom maior**,
**de baixo = relativa menor**.

Os traços verticais caem nas **casas-limite**, que pertencem às duas formas vizinhas —
é por isso que as formas se emendam em vez de ficarem soltas.

### Em que casa eu estou
Na borda de baixo da régua há **uma janela por coluna**. Cada uma mostra um quadrado
partido na diagonal com **duas** casas: em cima, azul, a casa de 1 a 12; embaixo, laranja,
a gêmea de 13 a 24. São a mesma forma, 12 casas de distância.

Isso resolve a confusão mais comum da peça: a régua mostra **uma oitava do tom maior**,
então em `C / Am` ela cobre as casas 8 a 20. A tônica de Am fica 3 casas antes do C, na
casa 5 — fora da janela. Por isso a **forma 1 de Am aparece na casa 17**, e não na 5.
Não é outra forma: 17 − 12 = 5.

Na 6ª corda os **dois quadrados** ficam a 12 casas de distância: de um ao outro é uma
oitava — ali a escala fecha e recomeça.

### Ver uma forma só — as cortinas
As duas cortinas correm no canal de baixo, **entre o papel e a régua**. Elas tapam o
papel, então pelos furos da régua você vê a chapa lisa delas em vez da nota.

Empurre uma de cada lado até se encontrarem em volta da forma que quer estudar: só aquela
caixa fica viva, o resto do braço apaga. Para ver tudo de novo, empurre as duas para as
pontas.

Cada cortina tem um rasgo em cima e outro embaixo, então a **tabela das formas e o número
das casas continuam visíveis** o tempo todo — e os rasgos são onde você põe o dedo para
empurrar (não há pega saliente, ela bateria na régua).

Nada disso é texto gravado no plástico: a legenda completa está no rodapé da folha A4.

É a mesma peça porque a menor natural usa as mesmas notas da relativa maior — o mesmo motivo pelo qual a roda mostra os dois campos.

## Os furos
| Furo | O que é |
|---|---|
| Quadrado grande | tônica maior |
| Losango | tônica menor relativa |
| Círculo | nota da pentatônica |
| **Triângulo** | graus 4 e 7 — só na escala completa |

Ignorando os triângulos você toca pentatônica; usando todos os furos, a escala completa.

## As 5 formas
A tabela no topo da régua é uma **etiqueta de papel** (130 × 13 mm) colada num rebaixo —
sai colorida, uma cor por forma, em vez de gravada no plástico. Ela está na página 2 do
`arte-trilho.pdf`, com uma cópia de reserva.

É uma grade de 5 caixas. **Linha de cima = numeração
para tom maior, linha de baixo = para a relativa menor** — as formas são as mesmas, muda
só por onde você começa a contar:

| maior | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **menor** | 2 | 3 | 4 | 5 | 1 |

Os traços verticais caem nas casas-limite, que pertencem às **duas** formas vizinhas — é
por ali que você emenda uma na outra sem parar a frase.

## Por que funciona nos 12 tons
Porque o espaçamento das casas é **uniforme** — não é maquete de braço real. Deslizar 1 casa = subir 1 semitom, e o desenho continua batendo. Num braço de verdade, onde o espaçamento é logarítmico, isso não funcionaria.

## Ajustes (`.scad`)
- Régua presa no canal → `SH` de 95.2 para 94.8 (nível 2); cortina presa → `KH` de 96.4 para 96.0
- Régua ou cortina folgada → aumente `SH` / `KH` em 0,4 mm
- Balanço vertical → `H1` / `H2` de 2.1 para 2.0 (menos altura de canal)
- Rabo de andorinha frouxo → aumente a diferença `C1-T1` (hoje 1,3 mm de pega por lado)
- Peça maior/menor → mexa em `CW` e `RS` no `.scad` **e** no `arte_regua.py` (têm de bater)
- Papel mais grosso → `PAP` de 0.35 para a espessura do seu papel
- Outra afinação → `AFIN` (classe de altura, da corda grave para a aguda) no `.scad` **e** no `arte_regua.py`
