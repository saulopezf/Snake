import pygame, random

class Snake:
    def __init__(self):
        self.tail = []
        self.w = 20
        head_x = 400
        head_y = 300
        self.tail.append(pygame.Rect(head_x, head_y, self.w, self.w))
        self.tail.append(pygame.Rect(head_x-20, head_y, self.w, self.w))
        self.tail.append(pygame.Rect(head_x-40, head_y, self.w, self.w))
        self.tail.append(pygame.Rect(head_x-60, head_y, self.w, self.w))

    def get_x(self):
        return self.tail[0].x
    
    def get_y(self):
        return self.tail[0].y

    def get_head(self):
        return self.tail[0]
    
    def choque(self):
        x = self.tail[0].x
        y = self.tail[0].y
        for i in range(4,len(self.tail)):
            if self.tail[i].x == x and self.tail[i].y == y:
                return True
        return False

    def add_part(self):
        ultima_parte = len(self.tail) - 1 
        self.tail.append(pygame.Rect(self.tail[ultima_parte].x, self.tail[ultima_parte].y, self.w, self.w))


class Punto:
    def __init__(self):
        self.w = 20
        self.x = 100
        self.y = 100
    
    def get(self):
        return pygame.Rect(self.x, self.y, self.w, self.w)

    def nueva_posicion(self,snake,actual_screen_w,actual_screen_h):
        actual_screen_w = actual_screen_w - 1
        actual_screen_h = actual_screen_h - 1
        x = self.random_x(actual_screen_w)
        y = self.random_y(actual_screen_h)
        pos_snake = self.comprobar_punto_serpiente(snake,x,y)
        while pos_snake:
            x = self.random_x(actual_screen_w)
            y = self.random_y(actual_screen_h)
            pos_snake = self.comprobar_punto_serpiente(snake,x,y)
                
        self.x = x
        self.y = y
    
    def random_x(self,actual_screen_w):
        x = random.randint(0, actual_screen_w)
        while x % 20 != 0:
            x = random.randint(0, actual_screen_w)
        return x

    def random_y(self,actual_screen_h):
        y = random.randint(0, actual_screen_h)
        while y % 20 != 0:
            y = random.randint(0, actual_screen_h)
        return y

    def comprobar_punto_serpiente(self,snake,x,y):
        for snakePart in snake:
            if snakePart.x == x and snakePart.y == y:
                return True
        return False

def main():
    pygame.init()

    # Configuracion de la pantalla
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("SNAKE")

    # Obtener el ancho el largo de la pantalla
    info = pygame.display.Info()
    actual_screen_w = info.current_w
    actual_screen_h = info.current_h

    # Colores
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    
    # Snake props
    snake_vel = 20
    v = [snake_vel,0]

    # Inicializar serpiente y punto
    snake = Snake()
    punto = Punto()
    
    # Pintar primeros graficos
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, punto.get())
    for snakePart in snake.tail:
        pygame.draw.rect(screen, WHITE, snakePart)
    pygame.display.update()

    # FPS controller
    fps_controller = pygame.time.Clock()

    # Eventos
    MOVE_TIME = 100
    MOVE_SNAKE = pygame.event.Event(pygame.USEREVENT, attr1='MoveSnake')
    CHANGE_DIR = pygame.event.Event(pygame.USEREVENT, attr1='ChangeDirection')
    pygame.time.set_timer(MOVE_SNAKE, MOVE_TIME)

    # Bucle del juego
    run = True 
    partida = True
    dir_changed = False
    last_key = pygame.K_RIGHT
    while run:
        # Inicio partida
        if partida:

            # Lista de graficos
            pintar_graficos = []
            
            # Iteramos todos los eventos que hay en el tick actual
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and last_key!=pygame.K_RIGHT and last_key!=pygame.K_LEFT:
                        snake_vel = -abs(snake_vel)
                        v = [-abs(snake_vel),0]
                        last_key = pygame.K_LEFT
                        dir_changed = True
                    elif event.key == pygame.K_RIGHT and last_key!=pygame.K_LEFT and last_key!=pygame.K_RIGHT:
                        snake_vel = abs(snake_vel)
                        v = [abs(snake_vel),0]
                        last_key = pygame.K_RIGHT
                        dir_changed = True
                    elif event.key == pygame.K_UP and last_key!=pygame.K_DOWN and last_key!=pygame.K_UP:
                        snake_vel = -abs(snake_vel)
                        v = [0,-abs(snake_vel)]
                        last_key = pygame.K_UP
                        dir_changed = True
                    elif event.key == pygame.K_DOWN and last_key!=pygame.K_UP and last_key!=pygame.K_DOWN:
                        snake_vel = abs(snake_vel)
                        v = [0,abs(snake_vel)]
                        last_key = pygame.K_DOWN
                        dir_changed = True
                    if dir_changed:
                        pygame.event.post(CHANGE_DIR)
                        pygame.time.set_timer(MOVE_SNAKE, MOVE_TIME)
                        dir_changed = False
                elif event == CHANGE_DIR or event == MOVE_SNAKE:
                    i = 0
                    for snakePart in snake.tail:
                        x = snakePart.x
                        y = snakePart.y
                        if( i == 0 ): # Snake head
                            snakePart.move_ip(v)
                            pintar_graficos.append(snakePart)
                            pygame.draw.rect(screen, WHITE, snakePart)
                        elif ( i == (len(snake.tail)-1) ): # Snake end
                            delete_tail = [snakePart.x,snakePart.y,snakePart.w,snakePart.w]
                            pintar_graficos.append(delete_tail)
                            pygame.draw.rect(screen, BLACK, delete_tail)
                            snakePart.x = last_x
                            snakePart.y = last_y
                        else:
                            snakePart.x = last_x
                            snakePart.y = last_y
                        i += 1
                        last_x = x
                        last_y = y
                    
                    x = snake.get_x()
                    y = snake.get_y()

                    # Se choca contra la pared || Contra el mismo
                    if (x<0 or x>=actual_screen_w or y<0 or y>=actual_screen_h) or (snake.choque()):
                        partida = False
                        continue

                    # Si se come el punto genera uno nuevo
                    if(x == punto.x and y == punto.y):
                        snake.add_part()
                        punto.nueva_posicion(snake.tail,actual_screen_w,actual_screen_h)
                        pintar_graficos.append(punto.get())
                        pygame.draw.rect(screen, RED, punto.get())
                        
                    # Pintamos los graficos que han cambiado
                    pygame.display.update(pintar_graficos)

        # End partida
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: run = False
        
        # Controlador de fps
        fps_controller.tick()
        #print(fps_controller.get_fps())

    # End juego
    pygame.quit()

if __name__=="__main__":
    main()