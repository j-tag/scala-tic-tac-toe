import scala.collection.immutable.Range
import scala.collection.mutable.ListBuffer

@main def game: Unit =
  showBoard()
  println()
  var currentPlayer = selectPlayer()
  var gameFinished = false

  while (!gameFinished) {
    println(s"Player $currentPlayer should select: [1-9]")
    var spot = scala.io.StdIn.readInt()
    // Validate selection
    while (!isValidSelection(currentPlayer, spot)) {
      // Invalid selection so get value again
      println(
        "Invalid selection. Selection must be in range and not be duplicate. Select again:"
      )
      spot = scala.io.StdIn.readInt()
    }

    // Select spot for player
    selectSpot(currentPlayer, spot)
    // Check winner
    if checkWinner(currentPlayer) then {
      println(s">> Player $currentPlayer WINS! <<")
      // Indicate that the game is ended
      gameFinished = true
    }
    // Check draw
    if !gameFinished && checkDraw() then {
      println(">> Match DRAW! <<")
      // Indicate that the game is ended
      gameFinished = true
    }
    // Show current board
    showBoard()
    // Switch to next player
    currentPlayer = nextPlayer(currentPlayer)
  }

// Player types
enum Player:
  case X, O

// Game status
val board: ListBuffer[Option[Player]] = ListBuffer.fill(10)(None)

// Show curren game status
def showBoard(): Unit = {
  for (i <- 1 to 9) {
    val spot = spotViewer(i)
    print(s"$spot ")
    if (i % 3 == 0) {
      println()
    }
  }
}

// Returns view of a spot
def spotViewer(i: Int): String = board(i) match {
  case None           => "-"
  case Some(Player.X) => "X"
  case Some(Player.O) => "O"
}

// Select player for start
def selectPlayer(): Player = {
  val rand = new scala.util.Random
  if (rand.nextInt(2) == 1) Player.O else Player.X
}

// Select next player to switch turn
def nextPlayer(currentPlayer: Player): Player =
  if (currentPlayer == Player.X) Player.O else Player.X

// Acquire spot by player
def selectSpot(player: Player, spot: Int) = board(spot) = Some(player)

// Validate selection
def isValidSelection(player: Player, spot: Int): Boolean = {

// Check range
  if (spot < 1 || spot > 9) then return false

// Avoid duplicate selection
  if board(spot) != None then return false

  true
}

// Check for winner
def checkWinner(player: Player): Boolean = {
  var isWinner = false

  // Rows
  for (i <- 1 to 9 by 3) {
    if board slice (i, i + 3) forall (_ == Some(player)) then isWinner = true
  }

  // Columns
  for (i <- 1 to 3) {
    val indices = List(i, i + 3, i + 6)
    if indices map board forall (_ == Some(player)) then isWinner = true
  }

  // Diagonals
  val indices = List(1, 5, 9)
  if indices map board forall (_ == Some(player)) then isWinner = true
  val indices2 = List(3, 5, 7)
  if indices2 map board forall (_ == Some(player)) then isWinner = true

  isWinner
}

// Check for draw
def checkDraw(): Boolean = {
  !board.drop(1).contains(None)
}
