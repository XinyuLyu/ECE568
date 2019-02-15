import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;
import java.util.regex.Pattern;

public class server {
    public static void main(String[] args) throws IOException {
        //  System.out.println(args.length);
        if (args.length != 1) { // Test for correct num. of arguments
            System.err.println("ERROR server port number not given");
            System.exit(1);
        }
        int port_num = Integer.parseInt(args[0]);
        ServerSocket rv_sock = new ServerSocket(port_num);
//        try {
//            new ServerSocket(port_num);
//        } catch (IOException ex) {
//          //  ex.printStackTrace();
//        }
        while (true) { // run forever, waiting for clients to connect
            System.out.println("\nWaiting for client to connect...");
            try {
                Socket s_sock = rv_sock.accept();//the server blocks and waits indefinitely until a client makes connection at which time a Socket object is returned.
                while (true) {// keep loop
                    BufferedReader in = new BufferedReader(    // read from client
                            new InputStreamReader(s_sock.getInputStream())
                    );
                    PrintWriter out = new PrintWriter(    //send to client
                            new OutputStreamWriter(s_sock.getOutputStream()),
                            true);
                    String cmd = in.readLine();//read commands from the client
                    if (cmd.substring(0, 4).equals("EXIT")) {//if is EXIT<code> print the code
                        System.out.println(
                                "Client's message: " + cmd);
                        if (cmd.equals("EXIT")) {
                            System.out.println("Normal_Exits");
                            break;
                        } else {
                            System.out.println(cmd.substring(5, cmd.length() - 1));
                            break;
                        }
                    } else {
                        if (cmd.substring(0, 3).equals("GET")) {
                            System.out.println(
                                    "Client's message: " + cmd);
                            String filename = cmd.substring(4, cmd.length() - 1);
                            String[] a = readTxtFile(filename);// read the contents of txt file
                            for (String b : a) {//print the contents
                                System.out.println(b);
                            }
                            if(a[0].equals("ERROR:No Such File"))
                            {
                                out.println(a[0]);//if not files not found send feedback to the client
                            }
                            else {
   //                               out.println("Successfully get "+filename);// if find send back successfully get the file
                                for (String b : a) {//print the contents
                                    out.println(b);
                                }
                            }
                        } else if (cmd.substring(0, 6).equals("BOUNCE")) {
                            System.out.println(
                                    "Client's message: " + cmd);
                            String a = cmd.substring(7, cmd.length() - 1);
                            System.out.println(a);
                            out.println("Successfully bounce "+a);// if successfuely bounce send the feedback
                        }
                    }
                }
                s_sock.close();
            }
                catch(IOException ex){
            ex.printStackTrace();
        }
    }

}
//    public static String readToString(String fileName) {
//        String encoding = "UTF-8";
//        File file = new File(fileName);
//        Long filelength = file.length();
//        byte[] filecontent = new byte[filelength.intValue()];
//        try {
//            FileInputStream in = new FileInputStream(file);
//            in.read(filecontent);
//            in.close();
//          //  fileexit=true;
//        } catch (FileNotFoundException e) {
//            System.out.println("ERROR: no such file");
//           // fileexit=false;
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//        try {
//            return new String(filecontent, encoding);
//        } catch (UnsupportedEncodingException e) {
//            System.err.println("The OS does not support " + encoding);
//            e.printStackTrace();
//            return null;
//        }
//    }
    public static String[] readTxtFile(String filePath)//cited from https://hacpai.com/article/1472004508201?m=0
    {                                                     // read test txt
        try{

            File f = new File(filePath);
            Scanner s = new Scanner(f);
         //   fileexit=true;
            int ctr = 0;
            while(s.hasNextLine())
            {
                ctr++;
                s.nextLine();
            }
            String[] arr = new String [ctr];

            Scanner s1 = new Scanner(f);

            for (int i = 0; i < arr.length; i++)
                arr[i] = s1.nextLine();
            return arr;

        }
        catch (FileNotFoundException e) {
        //    flag=false;
            String[] b={"ERROR:No Such File"};
            return b;

           // return null;
        }
        catch(Exception e)
        {
            //System.out.println("File Not Exits");
            String[] b={"ERROR:No Such File"};
            return b;
        }
    }
}
