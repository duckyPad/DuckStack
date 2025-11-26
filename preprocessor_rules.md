* duckyScript 3 is preprocessed into Python-compatible code
* Uses built-in module to generate AST and symbol table 
* AST walked and symbols resolved to generate assembly and bytecode

## duckyScript Command Translation

### Comments

|Command|Action|Comments|
|:-:|:-:|:-:|
|`REM`<br>`//`|Skip|Only when **outside** `STRING` blocks|
|`REM_BLOCK`<br>`END_REM`|Skip||

### Typing

|Command|Action|Comments|
|:-:|:-:|:-:|
|`STRING`<br>`STRINGLN`|Replace content with ds_string()|Escape all quotation marks?|
|`STRING_BLOCK`<br>`END_STRING`<br>`STRINGLN_BLOCK`<br>`END_STRINGLN`|Add triple quotes, ds_string()?|Escape all quotation marks|


-----


|Command|Action|Comments|
|:-:|:-:|:-:|
||||

## Printing Numbers

Currently `0x1f` escaped, static address.

What happens when printing function args?

may need to pop them on stack, then string instruction pops off when encounters a special escape character?

## String optimization

put into a dict as before
block strings no longer split into single lines, saves space

## Preprocessing Steps

Need to think of ordering

* Record the original line number starting from 1

* `DEFINE`: Find and replace as-is.

* `GOTO_PROFILE`: Replace name with profile index. Needs profile list info.

* `STRING_BLOCK` `END_STRING` `STRINGLN_BLOCK` `END_STRINGLN`: Replace with triple quotes for python string?

* 
