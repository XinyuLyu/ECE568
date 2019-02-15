import java.util.regex.Pattern;

public class test {
    public static void main(String[]args) {
        String input = "goog_history_price";
        String []a=input.split("_");
       String company=a[0];
       String typr=a[1];
        System.out.println("Company: "+a[0]+" Type: "+a[1]);

//    if (isMatch) {// valid command
//        if (input.substring(0, 4).equals("EXIT")) {
//            out.println(input);
//            break;/
//        }
//        if (input.substring(0, 3).equals("GET")) {
//            out.println(input);
//            String feedback = in.readLine();
//            System.out.println("Server says: " + feedback);
//        }
    }
}

