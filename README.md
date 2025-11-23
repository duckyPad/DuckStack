# DuckStack

|Addr|Purpose|Comment|
|:---:|:---:|:---:|
|`0000`<br>`EFFF`|Binary<br>Executable|60K Bytes|
|`F000`<br>`F7FF`|Data<br>Stack|2048 Bytes<br>4 Bytes Per Entry<br>512 Entries|
|`F800`<br>`F9FF`|Call<br>Stack|512 Bytes<br>2 Bytes Per Entry<br>256 Entries|
|`FA00`<br>`FBFF`|User-defined<br>Variables|512 Bytes<br>4 Bytes Per Entry<br>128 Entries|
|`FC00`<br>`FD7F`|Unused|384 Bytes|
|`FD80`<br>`FDFF`|NV<br>Global<br>Variables|128 Bytes<br>4 Bytes Per Entry<br>32 Entries|
|`FE00`<br>`FFFF`|Reserved<br>Variables|512 Bytes<br>4 Bytes Per Entry<br>128 Entries|

New entries all **grow towards larger address**.

## Changelog

* `VMVER` instruction: version number now on byte 1 (LSB)

