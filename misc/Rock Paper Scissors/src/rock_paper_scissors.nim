import std/[strformat, os, strutils]
import RC4

proc printFlag() =
  let ciphertext = "06077d19c166f9664697140dd5cf5fbd1980b20f2c949a0e1f0620dad71082d4de49"
  echo fromRC4("dynamite", ciphertext)

proc playerWins() =
  echo "💥 BOOOOOOOM!"
  sleep(1000)
  echo "😱 Wait! That wasn't part of the rules!"
  sleep(1000)
  printFlag()

proc computerWins() =
  echo "[#] Unlucky! I knew I would win"
  sleep(1000)
  echo "[#] Better luck next time!"
  sleep(1000)

proc determineWinner(computerChoice, playerChoice: string) =
  echo &"[#] You chose: {playerChoice}"
  sleep(1000)
  
  if playerChoice == "dynamite":
    playerWins()
    return
  
  echo &"[#] I choose: {computerChoice}"
  sleep(1000)
  computerWins()

proc getComputerChoice(playerChoice: string): string =
  case playerChoice
  of "rock":     "paper"
  of "paper":    "scissors"
  of "scissors": "rock"
  of "dynamite": ""
  else:          ""

proc main() =
  echo "[#] Hello friend..."
  sleep(1000)
  echo "[#] Welcome to rock, paper, scissors!"
  sleep(1000)
  echo "[#] Let's play!"
  sleep(1000)
  
  while true:
    stdout.write("[>] Enter your choice (rock, paper, scissors): ")
    let playerChoice = readLine(stdin).strip().toLowerAscii()

    if playerChoice in ["rock", "paper", "scissors", "dynamite"]:
      let computerChoice = getComputerChoice(playerChoice)
      determineWinner(computerChoice, playerChoice)
      break
    else:
      echo "[!] Invalid choice. Try again."

when isMainModule:
  main()
