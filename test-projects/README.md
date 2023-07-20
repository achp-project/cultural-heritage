# Comparing Resource Models

Given Arches Resource Models (RM) CIDOC-CRM compliants coming from different projects, the aim is to identify which edges are commons subgraphs (ie, same minimal common semantisation)

## Pairwise comparison


<p align="center">
  <img alt="img-name" src="../www/rm-compar-g1.png" width="500">
  <img alt="img-name" src="../www/rm-compar-g2.png" width="500">
  <br>
    <em>Comparison between G1 and G2</em>
</p>

The only common subgraph between G1 and G2 is

```mermaid
flowchart LR
    A((E39)):::pydef --P3--> B((E55)):::pydef;
	classDef pydef fill:#1f78b4;
```
Indeed:
* the second edges (`E55` -- `E2`) have different proprieties (`P4` and `P1`);
* the third edges (`E2` -- `E7`) have the same proprieties (`P5`) but different directions (`E2` --> `E7`; `E2` <-- `E7`)

The dataframe view of G1 is:

|    | source   | target   | property   |
|---:|:---------|:---------|:-----------|
|  0 | E39      | E55      | P3         |
|  1 | E55      | E2       | P4         |
|  2 | E2       | E7       | P5         |

The dataframe view of G2 is:

|    | source   | target   | property   |
|---:|:---------|:---------|:-----------|
|  0 | E39      | E55      | P3         |
|  1 | E55      | E2       | P4         |
|  2 | E2       | E7       | P5         |

The common row (ie common subgraph) between G1 and G2 is:

|    | source   | target   | property   |
|---:|:---------|:---------|:-----------|
|  0 | E39      | E55      | P3         |


