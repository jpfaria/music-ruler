# Régua de escalas — trilho + régua deslizante

Mesma lógica da roda: uma camada fixa com toda a informação, uma camada móvel que recorta.

## Imprimir
| Peça | Tamanho | Peso |
|---|---|---|
| `regua_1-TRILHO.stl` | 280 × 108 × 6,6 mm | ~53 g |
| `regua_2-REGUA-DESLIZANTE.stl` | 154 × 96 × 2,4 mm | ~12 g |

Sem suporte. Bico 0,4 · camada 0,16 · 3 perímetros · 20 %. **PETG.** O trilho tem 280 mm — use **brim de 5 mm**, mesa a 80 °C e a câmara fechada, senão as pontas levantam.

`arte-trilho.pdf` — **A4 DEITADO**, 100 % / tamanho real. Página 1 traz os dois painéis, página 2 a legenda. Recorte um dos dois retângulos (o outro é reserva) e cole no rebaixo do trilho. As abas laterais seguram a régua; ela entra deslizando por uma das pontas.

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
Na borda de baixo da régua há **uma janela por coluna**. Cada uma mostra o número da casa
impresso no papel. As casas com marcador (3, 5, 7, 9, 12, 15, 17, 19, 21, 24) vêm com o
número em pastilha preta.

Na 6ª corda os **dois quadrados** ficam a 12 casas de distância: de um ao outro é uma
oitava — ali a escala fecha e recomeça.

Nada disso é texto gravado no plástico: a legenda completa está no rodapé da folha A4.

É a mesma peça porque a menor natural usa as mesmas notas da relativa maior — o mesmo motivo pelo qual a roda mostra os dois campos.

## Os furos
| Furo | O que é |
|---|---|
| Quadrado grande | tônica maior |
| Losango | tônica menor relativa |
| Círculo grande | nota da pentatônica |
| Círculo pequeno | só na diatônica (4 e 7) |

Ignorando os círculos pequenos você toca pentatônica; usando todos, a escala completa.

## As 5 formas
Os colchetes gravados marcam as 5 formas. **Em cima a numeração para tom maior, embaixo para tom menor** — as formas são as mesmas, muda só por onde você começa a contar (a forma 1 do menor é a forma 5 do maior).

Os colchetes são escalonados em duas alturas de propósito: formas vizinhas compartilham uma casa, e assim dá pra ver a sobreposição.

## Por que funciona nos 12 tons
Porque o espaçamento das casas é **uniforme** — não é maquete de braço real. Deslizar 1 casa = subir 1 semitom, e o desenho continua batendo. Num braço de verdade, onde o espaçamento é logarítmico, isso não funcionaria.

## Ajustes (`.scad`)
- Régua folgada demais → `SH` de 96.4 para 97.0, ou `CH` de 2.6 para 2.4
- Régua presa → `SH` para 96.0 e `CH` para 2.8
- Peça maior/menor → mexa em `CW` e `RS` no `.scad` **e** no `arte_regua.py` (têm de bater)
- Aba caindo na impressão → `LT` de 1.0 para 1.4, ou `LIP` de 47.1 para 47.6 (menos balanço)
- Papel mais grosso → `PAP` de 0.35 para a espessura do seu papel
- Outra afinação → `AFIN` (classe de altura, da corda grave para a aguda) no `.scad` **e** no `arte_regua.py`
