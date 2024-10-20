'''
Credits to the Creators of Flappy bird for the inspiration of this game. 

Rough Idea:
- The warp pipes come from the left and are the ones moving toward the bird 
- They will have to be moving toward the left (some how animated)
- Every amount of seconds, a new version of tubes spawn (
- for the bird implementation, the bird just moves up and down, waiting for the warp pipes to come closer
- if space is not clicked, then the bird should start by falling... 
- create bounds + if the bird touches the warp pipes

extensions...
Increasing difficulty
high score - five players


'''

import turtle
import random

#To incorporate a starting screen
class StartScreen:
    def __init__(self):
        self.screen = turtle.getscreen()
        turtle.hideturtle()
        self.screen.setup(600, 400)
        self.screen.tracer(False)
        self.screen.bgcolor("skyblue")

        #main screen text
        self.turtleDrawer = turtle.Turtle()
        self.turtleDrawer.hideturtle()
        self.turtleDrawer.write("Fly Snorlax 🥱", False, "center", ("Times New Roman", 40, 'bold'))

        self.turtleDrawer.penup()
        self.turtleDrawer.goto(0, -30)
        self.turtleDrawer.write("Press Space to play!", False, "center", ("Playfair Display", 25, 'bold'))
        self.screen.update()

        file = open("FlyingBirdScore.txt", "r")
        wholeText = file.read()
        file.close()
        

        self.turtleDrawer.goto(0, 50)
        self.turtleDrawer.write("HIGH SCORES: \n" + wholeText,  False, "center", ("Times New Roman", 15, 'bold'))  

        self.screen.onkey(self.startGame,"space")
        self.screen.listen()
        self.screen.mainloop()

    #to being the game when space is pressed
    def startGame(self):
        self.screen.clear()
        FlyingBird()

#The main class... where the game is built
class FlyingBird:
    def __init__(self):
        #register the elements/shapes for the game to occur
        turtle.register_shape("snorlax.gif")
        turtle.register_shape("warppipeup.gif")
        turtle.register_shape("warppipedown.gif")
        self.player = turtle.Turtle("snorlax.gif")

        #to set up the score
        self.scoreDrawer = turtle.Turtle()
        self.scoreDrawer.hideturtle()
        self.score = 0

        #set up the screen
        self.screen = self.player.getscreen()

        self.screen.setup(600, 400)
        self.screen.tracer(False)
        self.started = True

        #position the player
        self.player.penup()
        self.player.goto(-200, 0)
        self.player.setheading(90)
        self.screen.update()
        self.pipes = []
        self.ychange = 0


        #methods to call
        self.setupEvents()

        self.makePipes()
        self.moveWarpPipes()
        self.screen.mainloop()

    #Responsible  for the game events, for instance, the keyboard callback events
    def setupEvents(self):
        self.screen.onkeypress(self.Jump, "space")
        self.screen.onkeypress(turtle.bye, "q")
        self.Move()
        self.screen.listen()

    #When the space bar is pressed, the player should move forwards 
    def Jump(self):
        #self.player.setheading(90)
        #when space is pressed, the y-coordinate of the player should increase by 10
        self.ychange = 10
        self.screen.update()

    #to draw the score on the screen
    def drawScore(self):
        self.scoreDrawer.clear()
        self.scoreDrawer.color("black")
        self.scoreDrawer.penup()
        self.scoreDrawer.goto(0, 130)
        self.scoreDrawer.pendown()
        self.scoreDrawer.write(int(self.score), False, "center", ("Times New Roman", 60, 'bold'))

    #The move function, for when the player is asked to jump
    def Move(self):
        if self.started:
            self.player.forward(self.ychange)
            #when space is not pressed, the y-coordinate should decrease by 5, so it seems like the
            #player is always falling unless space is pressed
            self.ychange -= 5
            self.collisionCheck()
            self.checkPipesLocation()
            if self.score % 7 ==0:
                self.screen.bgpic("haikyuu.gif")
            elif self.score % 5 == 0 or self.score % 13 == 0:
                self.screen.bgpic("naruto.gif")
            elif self.score % 6 == 0 or self.score % 9 ==0:
                self.screen.bgpic("snoopy.gif")
            elif self.score % 8 == 0 or self.score % 11 == 0: 
                self.screen.bgpic("totoro.gif")
            self.screen.update()
            self.screen.ontimer(self.Move, 100)

    #to see if the player touches the boundaries, if so, the game should stop
    def collisionCheck(self):
        if self.player.ycor() > self.screen.window_height()/2  or self.player.ycor() < -self.screen.window_height()/2:
            self.endScreen()
    
    #the end screen title when the player touches one of the warp pipes/boundaries
    def endScreen(self):
        self.screen.clear()
        self.screen.tracer(False)
        self.started = False
        self.screen.bgcolor("skyblue")
        
        #end screen text
        turtleDrawer = turtle.Turtle()
        turtleDrawer.hideturtle()
        turtleDrawer.penup()
        turtleDrawer.goto(0,60)
        turtleDrawer.write("Your score: " + str(self.score), False, "center", ("Times New Roman", 20, 'bold'))
        turtleDrawer.penup()
        turtleDrawer.goto(0,0)
        turtleDrawer.color("firebrick")
        turtleDrawer.write("GAME OVER!", False, "center", ("Times New Roman", 60, 'bold'))
        turtleDrawer.penup()
        turtleDrawer.goto(0, -25)
        turtleDrawer.color("black")
        turtleDrawer.write("Play again? Press Space! If not, 'q' to quit", False, "center", ("Times New Roman", 30, 'bold'))


        #to display the best three scores
        file = open("FlyingBirdScore.txt", "r")
        wholeText = file.read()
        allLines = wholeText.split("\n")
        file.close()
        #to check each score listed in the high scores
        if self.score > (float(allLines[0])):
            file = open("FlyingBirdScore.txt", "w")
            allLines.insert(0, str(self.score))
            allLines.pop()
            file.write("\n".join(allLines))
            file.close()
        elif self.score > (float(allLines[1])):
            file = open("FlyingBirdScore.txt", "w")
            allLines.insert(1, str(self.score))
            allLines.pop()
            file.write("\n".join(allLines))
            file.close()
        elif self.score > (float(allLines[2])):
            file = open("FlyingBirdScore.txt", "w")
            allLines.insert(2,str(self.score))
            allLines.pop()
            file.write("\n".join(allLines))
            file.close()

        #to restart the game
        self.screen.onkey(self.restartGame, "space")
        self.setupEvents()
        self.screen.listen()
        self.screen.mainloop()

    #the creation of the pipes
    def makePipes(self):
        if self.started:
            #to set each pipe at the right; so they start at the right and come into the screen, by moving left
            upPipe = turtle.Turtle("warppipeup.gif")
            upPipe.setheading(180)
            upPipe.penup()
            upPipe.goto(300, -270 + random.randint(-70, 80))
            self.pipes.append(upPipe)

            downPipe = turtle.Turtle("warppipedown.gif")
            downPipe.setheading(180)
            downPipe.penup()
            downPipe.goto(300, 300 + random.randint(-15, 50))
            self.pipes.append(downPipe)

            self.screen.update()
            self.screen.ontimer(self.makePipes, 1000)

    #to check if the player collides with one of the pipes
    def pipesCollisionCheck(self):
        for pipes in self.pipes:
            if self.player.distance(pipes.pos()) < 220:
                self.endScreen()
                break

    #for the score to be updated, the player and pipes should have the same x-coordinate
    def checkPipesLocation(self):
        for pipes in self.pipes:
            if pipes.xcor() < -380:
                self.pipes.remove(pipes)
                self.score += .5
                self.drawScore()

    #to move the warp pipes so they come to the player
    def moveWarpPipes(self):
        if self.started:
            if self.score < 5:
            #the pipes move to the left by 20 every time the screen updates
                for pipe in self.pipes:
                    pipe.forward(20)
            elif self.score >= 5:
                for pipe in self.pipes:
                    pipe.forward(15 + self.score)

            self.screen.update()

            self.pipesCollisionCheck()
            self.screen.ontimer(self.moveWarpPipes, 40)

    #to allow the user to restart the game if they lose
    def restartGame(self):
        self.screen.clear()
        StartScreen()



    
if __name__ == "__main__":
    #FlyingBird()
    StartScreen()

