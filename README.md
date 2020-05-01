# Bond-Creator
A program to display chemical bonds for simple compounds given the compounds equation.
<br>
## Example:
```python
bond('HCOOH')
```
### Output:
```bash
[[0, [1, 1]], [1, [0, 1], [3, 1], [2, 2]], [2, [1, 2]], [3, [4, 1], [1, 1]], [4, [3, 1]]]
bond
      ['C']
        |
      ['H']
bond
      ['H']
        |
['O']-['C']=['O']
bond
      ['C']
        ||
      ['O']
bond
      ['H']
        |
['C']-['O']
bond
      ['O']
        |
      ['H']
```

```python
bond('H2NOH')
```
### Output:
```bash
[[0, [2, 1]], [1, [2, 1]], [2, [0, 1], [1, 1], [3, 1]], [3, [4, 1], [2, 1]], [4, [3, 1]]]
bond
      ['N']
        |
      ['H']
bond
      ['N']
        |
      ['H']
bond
      ['H']
        |
['H']-['N']-['O']
bond
      ['H']
        |
['N']-['O']
bond
      ['O']
        |
      ['H']
```

```python
bond('CO2')
```
### Output:
```bash
[[0, [1, 2], [2, 2]], [1, [0, 2]], [2, [0, 2]]]
bond
      ['O']
        ||
['O']=['C']
bond
      ['C']
        ||
      ['O']
bond
      ['C']
        ||
      ['O']
```

