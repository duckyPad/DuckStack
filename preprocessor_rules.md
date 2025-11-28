* duckyScript 3 is preprocessed into Python-compatible code
* Uses built-in module to generate AST and symbol table 
* AST walked and symbols resolved to generate assembly and bytecode



## Preprocessing Steps

Need to think of ordering

3 stages:

1. Replace defines, special key names, `REPEAT`s, etc, remove all comment, empty lines, indents, etc.

2. replace syntax into python, re-indent by tracking bracket levels.

* Record the original line number starting from 1

* `DEFINE`: Find and replace as-is.

* Duplicate `REPEAT` commands

* `GOTO_PROFILE`: Replace name with profile index. Needs profile list info.

* `STRING_BLOCK` `END_STRING` `STRINGLN_BLOCK` `END_STRINGLN`: Replace with triple quotes for python string?

* `DEFAULTDELAY`, `DEFAULTCHARDELAY`, `CHARJITTER`: turn into reserved var assignments

## duckyScript Command Translation


### Comments

|Command|Action|Comments|
|:-:|:-:|:-:|
|`REM`<br>`//`|Skip|Only when **outside** `STRING` blocks|
|`REM_BLOCK`<br>`END_REM`|Skip||

### Typing

|Command|Action|Comments|
|:-:|:-:|:-:|
|`STRING`<br>`STRINGLN`|Replace content with `ds_string()`|Escape all quotation marks?|
|`STRING_BLOCK`<br>`END_STRING`<br>`STRINGLN_BLOCK`<br>`END_STRINGLN`|Add triple quotes, `ds_string()`?|Escape all quotation marks|

### Special Keys

* If a line starts with a special key

* Convert into `KEYDOWN` and `KEYUP`, like already does.

* Include **mouse keys?**

### `KEYDOWN` / `KEYUP`

* Include **mouse keys**?

* Args: 1

### `REPEAT`

Duplicate last line

### `DELAY`

Call `ds_delay()`

### `DEFAULTDELAY`

Preprocess into reserved variable

### `DEFAULTCHARDELAY`

Preprocess into reserved variable

### `CHARJITTER n`

Preprocess into reserved variable

### `LMOUSE` `RMOUSE` `MMOUSE`

wrap in `ds_special_key()`?

### `MOUSE_MOVE X Y`

wrap in `ds_mouse_move()`?

2 args

### `MOUSE_WHEEL X`

wrap in `ds_mouse_scroll()`?

### `LOOP`

TBD

### `PREV_PROFILE` / `NEXT_PROFILE`

ds_profile_step()

### `GOTO_PROFILE`

ds_profile_goto()

### `OLED_CURSOR x y`
### `OLED_PRINT`
### `OLED_CLEAR`
### `OLED_CIRCLE`
### `OLED_LINE`
### `OLED_RECT`
### `OLED_UPDATE`
### `OLED_RESTORE`
### `SWC_SET n r g b`
### `SWC_FILL r g b`
### `SWC_RESET n`

-----

|Command|Action|Comments|
|:-:|:-:|:-:|
||||

## Printing Numbers

Currently `0x1f` escaped, static address.

What happens when printing function args?

maybe different separators?

`0x1f` wraps around global variables

`0x1e` wraps around FP-relative variables?

## String optimization

put into a dict as before
block strings no longer split into single lines, saves space
