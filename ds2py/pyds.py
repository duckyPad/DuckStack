ball_pos_x = _RANDOM_INT%100 + 10
ball_pos_y = _RANDOM_INT%100 + 10
ball_velocity_x = 4
ball_velocity_y = 3
paddle_pos = 64
active_key = 0
score = 0
paddle_upper_limit = 30/2
paddle_lower_limit = 127-30/2
def update_paddle_position():
    if active_key == 25:
        paddle_pos = paddle_pos + 6
        if paddle_pos > paddle_lower_limit:
            paddle_pos = paddle_lower_limit
    if active_key == 24:
        paddle_pos = paddle_pos - 6
        if paddle_pos < paddle_upper_limit:
            paddle_pos = paddle_upper_limit
def draw_court():
    OLED_LINE(0, 0, 127, 0)
    OLED_LINE(0, 127, 127, 127)
    OLED_LINE(127, 0, 127, 127)
def draw_paddle():
    paddle_top_y = paddle_pos - 30/2
    paddle_bottom_y = paddle_pos + 30/2
    OLED_RECT(0, paddle_top_y, 2, paddle_bottom_y, 1)
def draw_ball():
    drawx = ball_pos_x
    drawy = ball_pos_y
    if drawx >= 127-2  or  drawx <= 2:
        return 
    if drawy >= 127-2  or  drawy <= 2:
        return 
    OLED_CIRCLE(drawx, drawy, 2, 1)
def draw_gameover():
    SWC_FILL(255, 0, 0)
    OLED_CLEAR()
    draw_paddle()
    draw_court()
    draw_ball()
    OLED_CURSOR(20, 40)
    OLED_PRINT('GAME OVER')
    OLED_CURSOR(20, 60)
    OLED_PRINT('Score: $score')
    OLED_UPDATE()
    BCLR()
    while 1:
        if _BLOCKING_READKEY <= 20:
            SWC_RESET(99)
            HALT()
def speed_up_ball():
    if ball_velocity_x >= 0:
        ball_velocity_x = ball_velocity_x + (_RANDOM_INT % 2)
    elif ball_velocity_x < 0:
        ball_velocity_x = ball_velocity_x - (_RANDOM_INT % 2)
    if ball_velocity_y >= 0:
        ball_velocity_y = ball_velocity_y + (_RANDOM_INT % 2)
    elif ball_velocity_y < 0:
        ball_velocity_y = ball_velocity_y - (_RANDOM_INT % 2)
def update_ball_pos():
    ball_pos_x = ball_pos_x + ball_velocity_x
    ball_pos_y = ball_pos_y + ball_velocity_y
    if (ball_pos_y >= 127 - 2*2)  or  (ball_pos_y <= 2*2):
        ball_velocity_y = ball_velocity_y * -1
    if ball_pos_x >= 127 - 2*2:
        ball_velocity_x = ball_velocity_x * -1
    if ball_pos_x <= 2*2:
        paddle_top = paddle_pos - 30/2
        paddle_bottom = paddle_pos + 30/2
        if ball_pos_y >= paddle_top  and  ball_pos_y <= paddle_bottom:
            ball_velocity_x = ball_velocity_x * -1
            score = score + 1
            speed_up_ball()
            SWC_FILL(_RANDOM_INT%255, _RANDOM_INT%255, _RANDOM_INT%255)
        else:
            ball_velocity_x = 0
            ball_velocity_y = 0
            draw_gameover()
SWC_FILL(0, 255, 0)
while 1:
    active_key = _READKEY
    update_paddle_position()
    update_ball_pos()
    OLED_CLEAR()
    draw_paddle()
    draw_court()
    draw_ball()
    OLED_UPDATE()
    DELAY(20)
