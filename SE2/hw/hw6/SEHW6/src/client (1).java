import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.regex.Pattern;

public class client {
    public static void main(String[] args) {
        if (args.length != 2) { // Test for correct num. of arguments
            System.err.println(
                    "ERROR server host name AND port number not given");
            System.exit(1);
        }
        int port_num = Integer.parseInt(args[1]);
            try {
                Socket c_sock = new Socket(args[0], port_num);
                while (true) {// keep loop
                    BufferedReader in = new BufferedReader(  //read from server
                            new InputStreamReader(c_sock.getInputStream())
                    );
                    PrintWriter out = new PrintWriter( //send to server
                            new OutputStreamWriter(c_sock.getOutputStream()),
                            true);
                    BufferedReader userEntry = new BufferedReader(// read user keyboard input
                            new InputStreamReader(System.in));
                    System.out.print("User, enter your message: ");
                    String input = userEntry.readLine();// get keyboard input
                    String pattern = "\\b(GET|BOUNCE|EXIT)\\b<.*>|\\bEXIT\\b";//judge if the command is valid by regular expressions
                    boolean isMatch = Pattern.matches(pattern, input);// judge if the input is valid
                    if (isMatch) {// valid command
                        if (input.substring(0, 4).equals("EXIT")) {
                            out.println(input);
                            break;// if EXIT break the loop and exit
                        }
                        if (input.substring(0, 3).equals("GET")) {
                            out.println(input);
                            String feedback = in.readLine();
                            System.out.println("Server says: " + feedback);
                        }
                        if (input.substring(0, 6).equals("BOUNCE")) {
                            out.println(input);
                            String feedback = in.readLine();
                            System.out.println("Server says: " + feedback);
                        }
                    } else {//invalid command
                        System.out.println("Invalid command");
                    }
                }
                c_sock.close();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
            System.exit(0);
        }
    }

