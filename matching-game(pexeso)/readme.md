 # Welcome to my matching game! (pexeso in slovak)
 
 ## In this game, you will be revealing images while trying to find pairs. If you find a match, pair remains revealed and you continue forward, otherwise the pair will hide itself. Reveal whole board! Good luck.

 ### Functionalities:
 - Board consisting of 32 squares, hiding image pairs
 - Upon first and second click on squares, they both reveal and game evaluates if they match:
   - match = images will stay revealed
   - mismatch = images will get hidden again
 - User can only click on hidden squares, clicking on revealed image doesn't do anything
 - At the bottom of game:
   - clickable button to stop the music
   - counter of mismatches
   - and highest local record (starting fresh at 1000, changing to users best score - lowest mismatches)
 - After user reveal whole board, he/she is asked to play another game or quit
 - If user starts a new game, whole board gets hidden, mismatches will reset to 0 and record is rewritten(if user scored better than previous record)
 - In download_link.txt you can find the game in .exe file, just extract files from downloaded .zip


 ## New game
![new_game](screenshots/new_game.jpg)


 ## Ongoing game
![ongoing](screenshots/ongoing.jpg)