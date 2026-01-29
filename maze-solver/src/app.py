import pygame

class App:
    def __init__(self):
        self._running = True
        self._display = None
        self.size = self.weight, self.height = 480, 480

    def on_init(self):
        pygame.init()
        self._display = pygame.display.set_mode(self.size, pygame.RESIZABLE | pygame.SCALED)
        self._running = True
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup():
        pygame.quit()
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

if __name__ == "__main__":
    theApp = App()
    theApp.onExecute()
