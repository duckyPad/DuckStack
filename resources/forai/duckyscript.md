duckyScript is a simple language for **automating keyboard/mouse inputs**.

## Comments

### `//`

C-style comment. Anything after `//` is ignored.

```
// This is a comment
```

### `REM`

BASIC/DOS/Win style comment. Works the same way.

```
REM This is a comment
```

### `REM_BLOCK` and `END_REM`

Comment block. Everything in-between is ignored.

```
REM_BLOCK
    Put as much comment here
    as you want!
END_REM
```

## Typing

### `STRING` and `STRINGLN`

`STRING` types out whatever after it **`AS-IS`**.

```
STRING Hello world!
// types out "Hello world!"
```

`STRINGLN` also presses **enter key** at the end.

### `STRINGLN_BLOCK` and `END_STRINGLN`

Type out everything inside as-is.

Also presses **enter key** at the end of each line.

```
STRINGLN_BLOCK

According to all known laws of aviation,
there is no way a bee should be able to fly.

END_STRINGLN
```

### `STRING_BLOCK` and `END_STRING`

Similar to above, but without new lines.

### Printing Variables / Print Formatting

See [Advanced Printing](#advanced-printing)

## Pressing Keys

### Special Keys

duckyScript supports many special keys.

They can be used on their own:

```
WINDOWS
```

...or combined with a character to form shortcuts:

```
WINDOWS s
```

...or chained even longer:

```
WINDOWS SHIFT s
```

------

* Type the key name **as-is** in **`ALL CAPS`**.

* Keys are pressed in sequence from **left-to-right**, then released **right-to-left**.

------

List of Special Keys:

``` 
  CTRL / RCTRL         |     (media keys)             
  SHIFT / RSHIFT       |     MK_VOLUP                 
  ALT / RALT           |     MK_VOLDOWN               
  WINDOWS / RWINDOWS   |     MK_MUTE                  
  COMMAND / RCOMMAND   |     MK_PREV                  
  OPTION / ROPTION     |     MK_NEXT                  
  ESC                  |     MK_PP (play/pause)       
  ENTER                |     MK_STOP                  
  UP/DOWN/LEFT/RIGHT   |                              
  SPACE                |     (numpad keys)            
  BACKSPACE            |     NUMLOCK                  
  TAB                  |     KP_SLASH                 
  CAPSLOCK             |     KP_ASTERISK              
  PRINTSCREEN          |     KP_MINUS                 
  SCROLLLOCK           |     KP_PLUS                  
  PAUSE                |     KP_ENTER                 
  BREAK                |     KP_0 to KP_9             
  INSERT               |     KP_DOT                   
  HOME                 |     KP_EQUAL                 
  PAGEUP / PAGEDOWN    |                              
  DELETE               |     (Japanese input method)  
  END                  |     ZENKAKUHANKAKU           
  MENU                 |     HENKAN                   
  POWER                |     MUHENKAN                 
  F1 to F24            |     KATAKANAHIRAGANA         

```

### `KEYDOWN` / `KEYUP`

Hold/release a key.

Allows more fine-grained control.

Can be used to input [Alt Codes](https://en.wikipedia.org/wiki/Alt_code) for special characters:

```
// types out ¼
KEYDOWN ALT
KP_1
KP_7
KP_2
KEYUP ALT
```

### `REPEAT`

Repeats the **last line** **`n`** times.

```
STRING Hello world
REPEAT 10
// types out "Hello world" 11 times (1 original + 10 repeats)
```

## Timing

### `DELAY`

Creates a pause (in milliseconds) in execution.

Useful for **waiting for UI to catch up**.

```
WINDOWS r
DELAY 1000 // wait 1000 milliseconds, or 1 second
STRING cmd
```

### `DEFAULTDELAY`

How long to wait between **`each input-generating command`**.

* Default: 20ms

```
DEFAULTDELAY 50
// Wait 50ms between each command below

ALT
DOWN
ENTER
```

### `DEFAULTCHARDELAY`

How long to wait between **`each letter`** when **`typing text`**.

* Default: 20ms
    * To type faster, set to around 10.

```
DEFAULTCHARDELAY 10
// Wait 10ms between each letter 

STRING Hello World!
```

### `CHARJITTER n`

Adds an **additional** random delay between 0 and `n` milliseconds after `each key stroke`.

Can make typing more human-like.

* Set to 0 to disable.

## Mouse

### Mouse Buttons

* `LMOUSE`: Click LEFT mouse button

* `RMOUSE`: Click RIGHT mouse button

* `MMOUSE`: Click MIDDLE mouse button

* Can be used with `KEYDOWN` / `KEYUP` commands.

### `MOUSE_MOVE X Y`

Move mouse cursor `X` pixels horizontally, and `Y` pixels vertically.

* For `X`, a positive number moves RIGHT, negative number moves LEFT.

* For `Y`, a positive number moves UP, negative number moves DOWN.

* Set to 0 if no movement needed.

* **Disable mouse acceleration** for pixel-accurate results

### `MOUSE_WHEEL X`

Scroll mouse wheel `X` lines.

* A positive number scrolls UP, negative number scrolls DOWN.

## Multiple Actions

`LOOP` command lets you to **assign multiple actions to one key**.

You can use it to toggle / cycle through several actions like this:

```
LOOP0:
STRINGLN first action

LOOP1:
STRINGLN second action

LOOP2:
STRINGLN third action
```

* When pressed, a counter increments, and the script at the corresponding loop is executed.

* Keep the code inside simple!

* For more complex needs, see [Loops](#loops) section below.

## Profile Switching

### `PREV_PROFILE` / `NEXT_PROFILE`

Switch to the previous / next profile.

### `GOTO_PROFILE`

Jump to a profile by name. **Case sensitive!**

This ends the current script execution.

```
GOTO_PROFILE NumPad
```

## OLED

### `OLED_CURSOR x y`

Set where to print on screen.

`x y`: Pixel coordinates between `0` and `127`.

Characters are **7 pixels wide, 10 pixels tall.**

Characters print from **top-left** corner.

### `OLED_PRINT`

`OLED_PRINT hello world!` 

Prints the message into display buffer at current cursor location.

### `OLED_CLEAR`

Clears the display buffer.

### `OLED_CIRCLE`

`OLED_CIRCLE x y radius fill`

* `x y`: Origin coordinate
* `radius`: In Pixels
* `fill`: 0 or 1

### `OLED_LINE`

`OLED_LINE x1 y1 x2 y2`
* `x1, y1`: Starting Point
* `X2, y2`: Ending Point

### `OLED_RECT`

`OLED_RECT x1 y1 x2 y2 fill`

* `x1, y1`: Starting Corner
* `X2, y2`: Ending Corner
* `fill`: 0 or 1

### `OLED_UPDATE`

Actually update the OLED.

You should use `OLED_CLEAR`, `OLED_CURSOR`, `OLED_PRINT`, etc, to set up the display, then use this to print it.

This is **much faster** than updating the whole screen for every change.

### `OLED_RESTORE`

Restore the default profile/key name display.

`OLED_UPDATE` **NOT NEEDED**.

## Per-Key RGB

### `SWC_SET n r g b`

Change LED color of a switch

Set `n` to 0 for current key.

Set `n` between 1 to 20 for a particular key.

`r, g, b` must be between 0 and 255.

### `SWC_FILL r g b`

Change color of **ALL** LEDs.

`r, g, b` must be between 0 and 255.

### `SWC_RESET n`

Reset the key back to default color.

Set `n` to 0 for current key.

Set `n` from 1 to 20 for a particular key.

Set `n` to 99 for all keys.

## Constants

You can use `DEFINE` to, well, define a constant.

It can be either **integer** or **string**.

The content is **replaced AS-IS** during preprocessing, very much like `#define` in C.

```
DEFINE MY_EMAIL example@gmail.com

STRING My email is MY_EMAIL!
```

## Variables

You can declare a variable using `VAR` command:

```
// Declaration
VAR spam = 0
VAR eggs = 10

// Assignment
spam = 20
```

* Variables are **signed 32-bit integers**.

* Variables declared at top level have **global scope** and can be accessed **anywhere**.

* Variables declared **inside a function** have **local scope** and is only accessible **within that function**.

    * **Shadowing:** Local variables take precedence over global variables with the same name.

    * **Naming**: Local variables cannot share names with function arguments.

### Persistent Global Variables

There are 32 pre-defined global variables that provides **non-volatile** data storage.

* `_GV0` to `_GV31`
* Available across **all profiles**
* Persists over reboots

### Internal Reserved Variables

Some variables are **always available**. They all start with an underscore `_`.

You can read them to obtain information, or write to adjust settings.

```
VAR status = _IS_NUMLOCK_ON
_RANDOM_MIN = 10
```

[Click Me for Full list](#reserved-variables)

### Operators

You can perform operations on constants and variables.

* 🚨 All ops are **SIGNED** BY DEFAULT
    * Set `_UNSIGNED_MATH = 1` to switch to **unsigned** arithmetic mode

⚠️ = Affected by current **Arithmetic Mode**

#### Mathematics

```
=       Assignment
+       Add       
-       Subtract  
*       Multiply  
/       ⚠️ Integer Division
%       ⚠️ Modulus   
**      Exponent
```

Example:

```
spam = 2+3
spam = eggs * 10
```

#### Comparison

All comparisons evaluate to **either 0 or 1**.

```
==        Equal                  
!=        Not equal              
>         ⚠️Greater than           
<         ⚠️Less than              
>=        ⚠️Greater than or equal  
<=        ⚠️Less than or equal   
```

#### Logical 

| Operator |          Name         | Comment                                                |
|:--------:|:---------------------:|--------------------------------------------------------|
|    `&&`    |      Logical AND      | Evaluates to 1 if BOTH side are non-zero, otherwise 0. |
|   `\|\|`   |       Logical OR      | Evaluates to 1 if ANY side is non-zero, otherwise 0.   |
|    `!`    |      Logical NOT      | Evaluates to 1 expression is 0, vice versa. |

#### Bitwise

```
&       Bitwise AND   
|       Bitwise OR    
^       Bitwise XOR
~       Bitwise NOT
<<      Left Shift    
>>      ⚠️Right Shift
            Signed Mode: Arithmetic Shift (sign-extend)
            Unsigned Mode: Logical Shift (0-extend)
```

### Expressions

You can use **constant, variable, or expressions** in commands.

```
VAR amount = 100
DELAY amount*2+5
```

## Advanced Printing

You can print **the value of variables** when using `STRING`, `STRINGLN`, and `OLED_PRINT`:

Add a **dollar symbol ($) before the variable name** to print it as number.

```
STRING The value is: $spam
```

### Print Format

Write to `_STR_PRINT_FORMAT` to adjust **how numbers are printed**.

|Value|Format|Example|
|:---:|:---:|:---:|
|0|Decimal Unsigned (default)|`65409`|
|1|Decimal Signed|`-127`|
|2|Hexadecimal Lower Case|`ff81`|
|3|Hexadecimal Upper Case|`FF81`|

```
VAR foo = 65409

_STR_PRINT_FORMAT = 0
STRINGLN The value is: $foo

_STR_PRINT_FORMAT = 1
STRINGLN The value is: $foo

_STR_PRINT_FORMAT = 2
STRINGLN The value is: $foo

_STR_PRINT_FORMAT = 3
STRINGLN The value is: $foo
```

```
The value is: 65409
The value is: -127
The value is: ff81
The value is: FF81
```

### Leading Zeros

Write to `_STR_PRINT_PADDING` to adjust **padding**.

* **Leading zeros** are added if the variable has fewer digits.

* Set to 0 for no padding.

* Works with all print formats.

```
_STR_PRINT_PADDING = 2

VAR year = 2025
VAR month = 8
VAR day = 5
STRING Date is: $year-$month-$day
```

```
Date is: 2025-08-05
```

## Real-time Clock (RTC)

duckyPad can keep track of **current date and time** for use in scripts.

### Setting RTC

On cold-boot, duckyPad doesn't know what time it is.

It must be set once, after which it will keep time **as long as it is powered-on**.

* RTC is **automatically set** when using the [Autoswitcher](https://github.com/duckyPad/duckyPad-Profile-Autoswitcher)

    * A **clock icon** appears when RTC is valid

    ![Alt text](../resources/photos/app/rtc.png)

* You can also set it manually

    * [HID Commands](https://github.com/duckyPad/duckyPad-Profile-Autoswitcher/blob/master/HID_details.md)

    * [Sample Script](https://github.com/duckyPad/duckyPad-Profile-Autoswitcher/blob/master/hid_example/ex3_set_rtc.py)

### Reading RTC

#### Validity Check

First, read `_RTC_IS_VALID`. **Do not proceed** if value is 0.

```
IF _RTC_IS_VALID == 0 THEN
    // RTC is uninitialised, do not proceed.
    HALT
END_IF
```

#### UTC Offset

The RTC always runs in **UTC**.

Local time is obtained by adding an **UTC Offset in `MINUTES`**

* It is **set automatically** to your **local timezone** when using the [Autoswitcher](https://github.com/duckyPad/duckyPad-Profile-Autoswitcher).

* You can check (and manually adjust) the offset by reading/writing `_RTC_UTC_OFFSET` variable

    * Can be positive, 0, or negative.

#### Time and Date

With valid RTC and correct UTC offset, you can now read from the variables below:

| Name      | Comment                | Range |
| ------------- | -------------------------- | --------------- |
| `_RTC_YEAR`  | **4-digit** Year          | e.g. `2025`    |
| `_RTC_MONTH` | Month              | `1–12`          |
| `_RTC_DAY`   | Day              | `1–31`          |
| `_RTC_HOUR`   | Hour | `0–23` |
| `_RTC_MINUTE` | Minute                | `0–59` |
| `_RTC_SECOND` | Second                | `0–60` |
| `_RTC_WDAY`  | Day of Week (`0 = Sunday`) | `0–6`           |
| `_RTC_YDAY`  | Day of Year (`0 = Jan 1`) | `0–365`           |

#### Example Usage

```
_STR_PRINT_PADDING = 2
STRINGLN _RTC_YEAR-_RTC_MONTH-_RTC_DAY _RTC_HOUR:_RTC_MINUTE:_RTC_SECOND
```

```
2025-09-18 09:07:23
```
## Conditional Statements

`IF` statement is used to conditionally execute code.

At simplest, it involves `IF`, `THEN`, and `END_IF`:

```
IF expression THEN
    code to execute
END_IF
```

The code inside is executed if the **expression evaluates to non-zero**.

Indent doesn't matter, feel free to add them for a cleaner look.

----

You can use `ELSE IF` and `ELSE` for additional checks.

If the first `IF` evaluate to 0, `ELSE IF`s are checked and executed if condition is met.

If none of the conditions are met, then code inside `ELSE` is executed.

```
VAR spam = 5

IF spam == 0 THEN
    STRING spam is zero!
ELSE IF spam == 1 THEN
    STRING spam is one!
ELSE
    STRING spam is none of those!
END_IF
```

## Loops

You can use `WHILE` loops to repeat instructions until a certain condition is met.

Syntax:

```
WHILE expression
    code to repeat
END_WHILE
```

If `expression` evaluates to zero, the code is skipped. Otherwise the code inside is repeated.

This simple example loops 3 times.

```
VAR i = 0
WHILE i < 3
    STRINGLN Counter is $i!
    i = i + 1
END_WHILE
```

```
Counter is 0!
Counter is 1!
Counter is 2!
```

### `LBREAK`

Use `LBREAK` to **exit a loop** immediately.

```
VAR i = 0
WHILE TRUE
    STRINGLN Counter is $i!
    i = i + 1

    IF i == 3 THEN
        LBREAK
    END_IF
END_WHILE
```
```
Counter is 0!
Counter is 1!
Counter is 2!
```

### `CONTINUE`

Use `CONTINUE` to **jump to the start of loop** immediately.

```
VAR i = 0
WHILE i < 5
    i = i + 1

    IF i == 3 THEN
        CONTINUE
    END_IF

    STRINGLN Counter is $i!
END_WHILE
```

Here when `i` is 3, it skips printing and starts from the top instead.

```
Counter is 1!
Counter is 2!
Counter is 4!
Counter is 5!
```

### Infinite Loop

To exit an infinite loop, you can [check button status](#reading-inputs), or turn on `Allow Abort` in configurator settings.

## Functions

Syntax:

```
FUNCTION func_name(arg1, arg2...)
    code
    ...
    RETURN
END_FUNCTION
```

* Up to 8 arguments
* Use **`RETURN`** to exit a function early
* Variables declared inside function have local scope
* 0 is returned without an explicit `RETURN` statement

## Reading Inputs

You can read the status of:

* Built-in Switches
* Rotary Encoders
* Expansion Module Switches

### Blocking Read

Simplest method.

Just read `_BLOCKING_READKEY` reserved variable.

It will block until a key is pressed.

```
VAR this_key = _BLOCKING_READKEY
// Waits here until a key is pressed

IF this_key == 1 THEN
    // do something here
ELSE IF this_key == 2 THEN
    // do something else
END_IF

```

### Non-Blocking Read

Read reserved variable `_READKEY`, returns immediately.

Returns 0 if no key is pressed. Key ID otherwise.

Check this in a loop to perform work even when no key is pressed.

```
VAR this_key = 0

WHILE TRUE
    this_key = _READKEY
    IF this_key == 1 THEN
        // handling button press
    END_IF

    // otherwise do work here
END_WHILE
```

### Switch Status Bitfield

Read reserved variable `_SW_BITFIELD`, returns immediately.

Each bit position stores the status of the corresponding key.

E.g. bit 1 = key ID 1, bit 13 = key ID 13, etc.

If that bit is 1, the key is held down.

You can use bitmasks to check multiple keys at once.

### Key ID

This is the number returned by methods above.

```
duckyPad Pro (2024):

1-20:
    * Built-in keys
    * Top left is 1
    * Bottom right is 20

21: Upper Rotary Encoder Clockwise
22: Upper Rotary Encoder Counterclockwise
23: Upper Rotary Encoder Push-down

24: Lower Rotary Encoder Clockwise
25: Lower Rotary Encoder Counterclockwise
26: Lower Rotary Encoder Push-down

27: Plus Button
28: Minus Button

37+: External Switches
```

```
duckyPad (2020):

1-15:
    * Top left is 1
    * Bottom right is 15
    * Plus button 16, Minus button 17.
```

## Randomisation

Read from `_RANDOM_INT` to get a random number.

By default, it is between 0 and 65535.

You can change the upper and lower bounds (**inclusive**) by writing to `_RANDOM_MAX` and `_RANDOM_MIN`.

```
_RANDOM_MIN = 0
_RANDOM_MAX = 100
STRINGLN Random number: _RANDOM_INT
```

## Miscellaneous

### `DP_SLEEP`

Make duckyPad go to sleep.

Backlight and screen are turned off.

Press any key to wake up.

### `HALT`

Stop execution immediately

## Reserved Variables

There are a few **reserved variables** that are always available.

You can read or write (RW) to adjust settings. Some are read-only (RO).

| Name                                                                 | Access | Description                                                                                    |
| --------------------------------------------------------------------------- | ----- | ---------------------------------------------------------------------------------------------- |
| **`_RANDOM_MIN`**<br>**`_RANDOM_MAX`**<br>**`_RANDOM_INT`**              | RW    | See [Randomisation](#randomisation)                                       |
| **`_TIME_S`**<br>**`_TIME_MS`**                                           | RO    | Elapsed time since power-on, in **seconds** or **milliseconds**.                               |
| **`_READKEY`**<br>**`_BLOCKING_READKEY`**                                 | RO    | See [Reading Inputs](#reading-inputs)                                      |
| **`_IS_NUMLOCK_ON`**<br>**`_IS_CAPSLOCK_ON`**<br>**`_IS_SCROLLLOCK_ON`** | RO    | Returns **1 if LED is on**, **0 otherwise**.                                                     |
| **`_DEFAULTDELAY`**<br>**`_DEFAULTCHARDELAY`**<br>**`_CHARJITTER`**      | RW    | Aliases.                               |
| **`_ALLOW_ABORT`**<br>**`_DONT_REPEAT`**                                  | RW    | **1 to enable**, **0 to disable**.                                      |
| **`_THIS_KEYID`**                                                          | RO    | Returns the [Key ID](#key-id) for the **current script**     |
| **`_DP_MODEL`**                                                            | RO    | Device model. Returns:<br>`1` for duckyPad (2020)<br>`2` for duckyPad Pro (2024)                              |
| **`_KEYPRESS_COUNT`**                                                      | RW    | Number of times the current key was pressed in the **current profile**.<br>Assign **0 to reset**. |
| **`_LOOP_SIZE`**                                                           | RO    | Used by the `LOOP` command.<br>Do not modify.                                                     |
| **`_NEEDS_EPILOGUE`**                                                      | RO    | Internal use only. Do not modify.                                                              |
|**`_RTC_IS_VALID`**<br>**`_RTC_YEAR`**<br>**`_RTC_MONTH`**<br>**`_RTC_DAY`**<br>**`_RTC_HOUR`**<br>**`_RTC_MINUTE`**<br>**`_RTC_SECOND`**<br>**`_RTC_WDAY`**<br>**`_RTC_YDAY`**|RO|See [Real-time Clock](#real-time-clock-rtc)|
|**`_RTC_UTC_OFFSET`**|RW|See [Real-time Clock](#real-time-clock-rtc)|
|**`_STR_PRINT_FORMAT`**<br>**`_STR_PRINT_PADDING`**<br>|RW|See [Advanced Printing](#advanced-printing)|
|**`_UNSIGNED_MATH`**|RW|Set to 1 to treat variables as **unsigned numbers** using **unsigned math**|
|**`_SW_BITFIELD`**|RO|Bit position corresponds to key ID.<br>1 = Pressed, 0 = released.|

