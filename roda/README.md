# Roda de campo harmônico

Uma peça só. Mecânica em 3D (lisa) + arte colorida em papel colada nos rebaixos.

## Imprimir
| Peça | Tamanho | Peso |
|---|---|---|
| `roda_1-DISCO-BASE.stl` | Ø117,9 × 13,0 mm | ~37 g |
| `roda_2-DISCO-GIRATORIO.stl` | Ø110 (+aba, 120,5) × 8,0 mm | ~19 g |

Sem suporte. Bico 0,4 · camada 0,2 · **3 perímetros** · 20 %. PETG de preferência.

`arte-COLORIDA.pdf` — A4, 100 % / tamanho real.
- **Base (Ø104):** recorte o círculo e o furo. C na seta vermelha, virado para a aba.
- **Disco (Ø108):** recorte o círculo, o furo e as 7 janelas brancas.

## Lendo
Cada janela traz duas pastilhas:

- **branca = grau no tom MAIOR**
- **preta = grau no tom MENOR relativo**

A chave está no próprio disco.

Cor da célula: 🟩 repouso · 🟧 transição · 🟥 tensão. Três acordes trocam de função entre os modos e saem bicolores:

| Acorde | Maior | Menor |
|---|---|---|
| F | transição (IV) | repouso (VI) |
| Em | repouso (III) | tensão (V) |
| B° | tensão (VII) | transição (II) |

## Editar
`COR=0 python3 arte.py` gera a versão P&B. O script trava se algum texto invadir linha de corte ou transbordar a célula.

## Antes de recortar o papel — CONFIRA A ESCALA
No rodapé da folha tem uma **barra de 100 mm**. Meça com régua.
Se não der 100 mm exatos, o PDF saiu reduzido: imprima de novo em **Escala 100% /
Tamanho real**, com “Ajustar à página” DESMARCADO. Deu X mm? Reimprima com escala
`100 × 100 ÷ X`. Os discos têm de sair com **104 mm** (base) e **108 mm** (de cima).

Era isso que fazia os acordes da borda não caírem dentro da janela.

## Miolo (encaixe)
O eixo de encaixe foi refeito: o ressalto agora tem **0,90 mm** de aba (era 0,45) e
nasce **0,5 mm acima do cubo**, então ele sempre sai do furo — a versão anterior
ficava presa dentro do furo e não segurava a tampa. Reimprima as duas peças.

Para montar: encaixe o disco de cima sobre o eixo e **aperte até ouvir o clique**.

## As duas tabelas de consulta
O disco de cima traz, dos dois lados do centro, as regras que todo mundo esquece:

- **TOM MAIOR** — `I(M) T II(m) T III(m) S IV(M) T V(M) T VI(m) T VII(°) S`
- **TOM MENOR** — `I(m) T II(°) S III(M) T IV(m) T V(m) S VI(M) T VII(M) T`

Cada caixa é um grau, com a qualidade do acorde dentro. A pastilha entre duas caixas é
o intervalo que separa elas — cinza = tom, roxo = semitom. A última pastilha fecha a
oitava, voltando ao I.

`T` = tom, `S` = semitom, `M` = maior, `m` = menor, `°` = diminuto.
