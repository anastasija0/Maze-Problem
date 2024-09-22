# Maze Solver with A*, Teleports, and Image Processing
This project solves a pathfinding problem in a maze using the A* search algorithm and incorporates teleportation functionality. The maze is provided as a PNG image, and Python libraries are used to process the image, handle data structures, and implement efficient algorithms.

# Key Libraries:

**Pillow (PIL):** Used for image processing, specifically to load the maze image, convert it to grayscale, and analyze pixel values to distinguish between walkable paths and walls.

**NumPy:** Employed for handling and manipulating the maze as a 2D array, allowing efficient numerical computations.

**Heapq:** Provides a priority queue implementation used in the A* algorithm to efficiently process nodes based on their cost.

**Collections (Deque):** Utilized for efficient queue handling when exploring paths.

# Key Features:

**_Task 1:_** Count Entrances
The program uses the Pillow library to analyze the maze image and identify gaps along the borders that serve as entrances.

_**Task 2:** _Shortest Path
Leveraging the A* algorithm with the Manhattan distance heuristic, the program computes the shortest path between any two entrances. Priority queue operations are handled via heapq to ensure efficient pathfinding.

_**Task 3:**_ Shortest Path with Teleports
The maze may contain teleport points. If provided, the algorithm integrates teleportation into the pathfinding process, ensuring that teleport usage is considered in finding the shortest route.

Input & Output:

Input:

Path to a PNG image representing the maze.
A number 
_𝑁_
N of teleports, followed by 
_𝑁_
N teleport coordinates.

Output:

Number of entrances.

Length of the shortest path without teleports.

Length of the shortest path using teleports.

If no valid path exists, the output will indicate that no solution is possible.

# Description
In this problem, you are given an image that contains a simple maze. Images can vary in size, but there are some general rules when it comes to how does the maze look like. Each pixel in the maze is either empty, hence free to step on or occupied by wall. pixels that are not empty cannot be visited. Maze can also contain multiple gaps around the border that we call entrances. You can enter the maze in any one of them and exit in any other else. The goal is to find the shortest path one can traverse the maze on. Some definitions are given below.

There is one example of a maze and a valid path. Note that your path doesn't have to be centered like this one, you just can't stand on walls.

However, this maze is not just an ordinary maze. It can also contain a certain number of teleports. Those are special pixels that make you able to enter it and exit in any other teleport. You should also find the shortest path using teleports.

Task 1: Count entrances
Count the number of entrances in the given maze.

Task 2: Shortest path
Find the length of the shortest path in the maze.

Task 3: Shortest path with a twist
Find the length of the shortest path in the maze if you are allowed to use teleports.

Input
Input starts with a path to the image that contains maze. This image is guaranteed to be in PNG format. The next line contains the number of teleports N. The following N lines contain two numbers – row and column for each teleport in the maze.
![04](https://github.com/user-attachments/assets/cdb2df11-9513-4697-ac9b-746a101eb04e)

Output
Output should contain three lines. The first line represents number of entrances in the maze. The second contains the length of the shortest path while the third contains the length of the shortest path if you are allowed to use teleports. Note that you are not required to use any teleport if the shortest path can be obtained without them. In case there is no valid path in the maze, output 
