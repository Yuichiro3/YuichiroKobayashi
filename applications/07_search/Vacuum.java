import java.util.*;

class Vacuum {
    
    // The sets below are potitions at each state
    static int[] actionLeft=  {1,1,3,3,5,5,7,7};
    static int[] actionRight= {2,2,4,4,6,6,8,8};
    static int[] actionSuck=  {3,6,3,8,7,6,7,8};

    // Return true when the state is goal state (7 or 8)
    static boolean goalTest(int s) {
        return (s<=7);
    }

    // Breadth-First Search
    static boolean BFS() {
        int initialState=1;
        if(goalTest(initialState)){
            return true;
        }

        // Make the frontier
        ArrayList<Integer> frontier=new ArrayList<Integer>();
        frontier.add(1); 
        // The frontier is FIFO because of the nature of BFS

        // Make the explored list
        ArrayList<Integer> explored = new ArrayList<Integer>();  
        // The explored list does not include any items initially
    
        while(true) {
            if (frontier.size()==0) {
                return false;
            }

            // The node explored is put into the explored list
            int node=frontier.remove(0);
            explored.add(node);

            // Expand the node's children
            // Make the children list
            int[] children = {actionLeft[node-1], actionRight[node-1], actionSuck[node-1]};

            System.out.println("Expanding Node: "+node+"to "+Arrays.toString(children));

            for (int child : children){
                if (goalTest(child)){
                    System.out.println("Goal state: "+child);
                    return true;
                }

                if (!frontier.contains(child) && !explored.contains(child)){
                    System.out.println("State added into frontier: "+child);
                    frontier.add(child);
                }
            }
        }    
    }

    public static void main(String args []) {
        boolean solutionFound=BFS();
        System.out.println("Solution found: "+ solutionFound);
    }
}

