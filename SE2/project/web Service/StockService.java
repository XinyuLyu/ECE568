  // written by:Xinyu Lyu
  // assisted by:all team Members
  // debugged by:all team Members
package stock.service;
import java.io.BufferedReader;
import stock.model.*;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.LineNumberReader;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import javax.ws.rs.core.Response;
import com.alibaba.fastjson.*;
import org.json.JSONObject;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import Jama.Matrix;
public class StockService {
		        private static String dbdriver = "com.mysql.jdbc.Driver";
		        private static String dburl = "jdbc:mysql://127.0.0.1:3306/xinyuDatabaseName?&useSSL=false";//cmx
		        private static String username = "root";
		        private static String userpassword = "yfj520520";
		        public static Connection conn = null;
		        public List<String> real_list = new ArrayList<String>();
		        public List<String> history_list = new ArrayList<String>();	 
		        public List<String> indicator = new ArrayList<>();
	public Response getLatestPrice(String userId)
	{
		getStockName(userId);
		JSONObject main = new JSONObject();
		List<JSONObject> list = new ArrayList<>();
    	for(int i=0;i<real_list.size();i++)
    	{
    	List<String>x1=GetData(userId,"select Open_Price from "+userId+"."+real_list.get(i)+"_realtime_price ORDER BY Date DESC limit 1;");
    	JSONObject company = new JSONObject();
    	company.put("price", x1.get(0));
    	company.put("company", real_list.get(i));
    	list.add(company);
    	}    
    	main.put("latest_Price",list);
		return Response.status(200).entity(main.toString()).build();
	}
	public Response getHighestPrice(String userId, String companyId)
	{
		getStockName(userId);
		JSONObject main = new JSONObject();
		List<JSONObject> list = new ArrayList<>();
		//main.put("company", companyId);
		if(history_list.contains(companyId))
		{
			List<String>x1=GetData("xinyu","select max(Q.Close_Price) from (select * from xinyu."+companyId+"_history_price P group by Date DESC limit 10) Q;");
	    	//List<String>x1=GetData(userId,"select max(Q.Close_Price) from (select * from "+userId+"."+companyId+"_history_price P group by Date DESC limit 10) Q;");
	    	JSONObject company = new JSONObject();
	    	company.put("price", x1.get(0));
	    	company.put("company", companyId);
	    	list.add(company);
		}
		main.put("HighestPrice", list);
		return Response.status(200).entity(main.toString()).build();
	}
	public Response getAveragePrice(String userId, String companyId)
	{
		getStockName(userId);
		JSONObject main = new JSONObject();
		List<JSONObject> list = new ArrayList<>();
		//main.put("company", companyId);
		if(history_list.contains(companyId))
		{
	    	List<String>x1=GetData(userId,"SELECT avg(Q.Close_Price) FROM (select * from "+userId+"."+companyId+"_history_price P group by Date DESC limit 252) Q;");
	    	JSONObject company = new JSONObject();
	    	company.put("price", x1.get(0));
	    	company.put("company", companyId);
	    	list.add(company);
	    	//main.put("AveragePrice", x1.get(0));
		}
		main.put("AveragePrice", list);
		return Response.status(200).entity(main.toString()).build();
	}
	public Response getLowestPrice(String userId, String companyId)
	{
		getStockName(userId);
		JSONObject main = new JSONObject();
		List<JSONObject> list = new ArrayList<>();
		
		if(history_list.contains(companyId))
		{
	    	List<String>x1=GetData(userId,"SELECT min(Q.Close_Price) FROM (select * from "+userId+"."+companyId+"_history_price P group by Date DESC limit 252) Q;");
	    	JSONObject company = new JSONObject();
	    	company.put("price", x1.get(0));
	    	company.put("company", companyId);
	    	list.add(company);
		}
		main.put("LowestPrice", list);
		return Response.status(200).entity(main.toString()).build();
	}
//	public Response lesserThanPrice(String userId, String companyId)
//	{
//		getStockName(userId);
//		JSONObject obj = new JSONObject();
//		String minPrice=GetData("xinyu","SELECT min(Close_Price) FROM "+userId+"."+companyId+"_history_price;").get(0);
//		double min=Double.parseDouble(minPrice);
//		for(int i=0;i<history_list.size();i++)
//		{
//			String averagePrice=GetData(userId,"SELECT avg(Close_Price) FROM "+userId+"."+history_list.get(i)+"_history_price;").get(0);
//	    	double avg=Double.parseDouble(averagePrice);
//	    	if(avg<min) {
//	           obj.put(history_list.get(i),averagePrice);
//	    	}
//		}
//		return Response.status(200).entity(obj.toString()).build();
//	}
	public Response lesserThanPrice(String userId, String companyId)
	{
		getStockName(userId);
		JSONObject Main = new JSONObject();

		JSONArray JsonArray = new JSONArray();
		List<JSONObject> list = new ArrayList<>();
		String minPrice=GetData("xinyu","SELECT min(Q.Close_Price) FROM (select * from "+userId+"."+companyId+"_history_price P group by Date limit 252) Q;").get(0);
		double min=Double.parseDouble(minPrice);
		for(int i=0;i<history_list.size();i++)
		{
			JSONObject obj = new JSONObject();
			String averagePrice=GetData("xinyu","SELECT avg(Q.Close_Price) FROM (select * from "+userId+"."+history_list.get(i)+"_history_price P group by Date limit 252) Q;").get(0);
	    	double avg=Double.parseDouble(averagePrice);
	    	if(avg<min) {
	           obj.put("price",averagePrice);
	           obj.put("company",history_list.get(i));
	           list.add(obj);
	    	}
	    	
	    	//JsonArray.add(obj);
		}
		
		//Main.put(companyId, JsonArray);
		Main.put(companyId, list);
		return Response.status(200).entity(Main.toString()).build();
	}
	public Response realtime(String userId, String companyId,String minutes)
	{
		getStockName(userId);
		JSONObject Main = new JSONObject();
		JSONArray JsonArray = new JSONArray();
		List<JSONObject> list = new ArrayList<>();
		//if(history_list.contains(companyId))
		//{
	    	List<String>date=GetData(userId,"SELECT Date FROM "+userId+"."+companyId+"_realtime_price P group by Date DESC limit "+minutes+";");
	    	//Data.put("Date", date);
	    	List<String>open_price=GetData(userId,"SELECT Open_Price FROM "+userId+"."+companyId+"_realtime_price P group by Date DESC limit "+minutes+";");
	    	//Data.put("Open_Price",open_price);
	    	List<String>high_price=GetData(userId,"SELECT High_Price FROM "+userId+"."+companyId+"_realtime_price P group by Date DESC limit "+minutes+";");
	    	//Data.put("High_Price",high_price);
	    	List<String>low_price=GetData(userId,"SELECT Low_Price FROM "+userId+"."+companyId+"_realtime_price P group by Date DESC limit "+minutes+";");
	    	//Data.put("Low_Price",low_price);
	    	List<String>close_price=GetData(userId,"SELECT Close_Price FROM "+userId+"."+companyId+"_realtime_price P group by Date DESC limit "+minutes+";");
	    	//Data.put("CLose_Price",close_price);
	    	List<String>h_volume=GetData(userId,"SELECT H_Volume FROM "+userId+"."+companyId+"_realtime_price P group by Date DESC limit "+minutes+";");
	    	//Data.put("H_Volume",h_volume);
	    	//int minVal=Integer.parseInt(minutes);
	    	for(int i=date.size()-1;i>=0;i--)
	    	{
	    		JSONObject Data1 = new JSONObject();
	    		Data1.put("Date", date.get(i));
	    		Data1.put("Open_Price",open_price.get(i));
	    		Data1.put("High_Price",high_price.get(i));
	    		Data1.put("Low_Price",low_price.get(i));
	    		Data1.put("CLose_Price",close_price.get(i));
	    		Data1.put("H_Volume",h_volume.get(i));
	    		list.add(Data1);
	    		// JsonArray.add(Data1);	   
	    	} 	
		//}
		Main.put(companyId,list);
		return Response.status(200).entity(Main.toString()).build();
	}
	public JSONObject getJsonObj(String name, String value) {  
	    JSONObject jsonobj = new JSONObject();  
	    jsonobj.put(name,value);  
	    return jsonobj;  
	}  
	public Response history(String userId, String companyId,String days )
	{
		getStockName(userId);
		JSONObject Main = new JSONObject();
		//Main.put("company",companyId);	
		//JSONObject Data = new JSONObject();
		List<JSONObject> list = new ArrayList<>();
		JSONArray JsonArray = new JSONArray();
		
	    	List<String>date=GetData(userId,"SELECT Date FROM "+userId+"."+companyId+"_history_price P group by Date DESC limit "+days+";");
	    //	Data.put("Date", date);
	    	List<String>open_price=GetData(userId,"SELECT Open_Price FROM "+userId+"."+companyId+"_history_price P group by Date DESC limit "+days+";");
	    //	Data.put("Open_Price",open_price);
	    	List<String>high_price=GetData(userId,"SELECT High_Price FROM "+userId+"."+companyId+"_history_price P group by Date DESC limit "+days+";");
	    //	Data.put("High_Price",high_price);
	    	List<String>low_price=GetData(userId,"SELECT Low_Price FROM "+userId+"."+companyId+"_history_price P group by Date DESC limit "+days+";");
	    //	Data.put("Low_Price",low_price);
	    	List<String>close_price=GetData(userId,"SELECT Close_Price FROM "+userId+"."+companyId+"_history_price P group by Date DESC limit "+days+";");
	    //	Data.put("CLose_Price",close_price);
	    	List<String>h_volume=GetData(userId,"SELECT H_Volume FROM "+userId+"."+companyId+"_history_price P group by Date DESC limit "+days+";");
	    //	Data.put("H_Volume",h_volume);
	    	for(int i=date.size()-1;i>=0;i--)
	    	{
	    		JSONObject Data1 = new JSONObject();
	    		Data1.put("Date", date.get(i));
	    		Data1.put("Open_Price",open_price.get(i));
	    		Data1.put("High_Price",high_price.get(i));
	    		Data1.put("Low_Price",low_price.get(i));
	    		Data1.put("CLose_Price",close_price.get(i));
	    		Data1.put("H_Volume",h_volume.get(i));
               list.add(Data1);
	    		// JsonArray.add(Data1);	   
	    	} 	
		
		Main.put(companyId,list);
		return Response.status(200).entity(Main.toString()).build();
	}	
	public  Response ANN(String companyId) throws IOException, InterruptedException {
		       JSONObject main = new JSONObject();    
		        String exe = "python";
		        String command = "C:\\Users\\admin\\Desktop\\Indicators & GetPrice\\Indicators & GetPrice\\ANN_short_term1.py";
		        String[] cmdArr = new String[] {exe,command,companyId};
	            Process proc=Runtime.getRuntime().exec(cmdArr); //执行py文件
	            InputStreamReader stdin=new InputStreamReader(proc.getInputStream());
	            LineNumberReader input=new LineNumberReader(stdin);
	            String line=input.readLine();
	            	String str1=line.replace("{","").replace("}", "");
	    	        String []jsonstr=str1.split(":");
	    	        jsonstr[1]=jsonstr[1].replace(" ", "");
	    	        jsonstr[0] =jsonstr[0].replace("\"","").replace("\"","");
	    	        main.put(jsonstr[0],jsonstr[1]);
	        return Response.status(200).entity(main.toString()).build();
	}
	public  Response LSTM(String companyId) throws IOException, InterruptedException {
		 JSONObject main = new JSONObject();    
		        String exe = "python";
		        String command = "C:\\Users\\admin\\Desktop\\Indicators & GetPrice\\Indicators & GetPrice\\LSTM1K.py";
		        String[] cmdArr = new String[] {exe,command,companyId};
	            Process proc=Runtime.getRuntime().exec(cmdArr); //执行py文件
	            InputStreamReader stdin=new InputStreamReader(proc.getInputStream());
	            LineNumberReader input=new LineNumberReader(stdin);
	            String line=input.readLine();	          
	            	String str1=line.replace("{","").replace("}", "");
	    	        String []jsonstr=str1.split(":");
	    	        jsonstr[1]=jsonstr[1].replace(" ", "");
	    	        jsonstr[0] =jsonstr[0].replace("\"","").replace("\"","");
	    	        main.put(jsonstr[0],jsonstr[1]);
	        return Response.status(200).entity(main.toString()).build();
	}
	public  Response SVM(String companyId) throws IOException, InterruptedException {
		        JSONObject main = new JSONObject();    
		        String exe = "python";
		        String command = "C:\\Users\\admin\\Desktop\\Indicators & GetPrice\\Indicators & GetPrice\\SVM.py";
		        String[] cmdArr = new String[] {exe,command,companyId};
	            Process proc=Runtime.getRuntime().exec(cmdArr); //执行py文件
	            InputStreamReader stdin=new InputStreamReader(proc.getInputStream());
	            LineNumberReader input=new LineNumberReader(stdin);
	            String line=input.readLine();
	            String str1=line.replace("{","").replace("}", "");
	    	    String []jsonstr=str1.split(":");
	    	    jsonstr[1]=jsonstr[1].replace(" ", "");
	    	    jsonstr[0] =jsonstr[0].replace("\'","").replace("\'","");
	    	    main.put(jsonstr[0],jsonstr[1]);
	        return Response.status(200).entity(main.toString()).build();
	}
	public  Response BYS(String companyId) throws IOException, InterruptedException {
        JSONObject main = new JSONObject();    
        bys BYS=new bys();
        String[] jsonstr=BYS.main(companyId);
	    //String []jsonstr=line.split(":");
	    //jsonstr[0] =jsonstr[0].replace("\"","").replace("\"","");
	    main.put(jsonstr[0],jsonstr[1]);
    return Response.status(200).entity(main.toString()).build();
}
	public static List<String> GetData(String ProjName, String sql)//1 function part(2)
	{
		Connection conn = getConn(ProjName);
	    PreparedStatement ps = null;
	    List<String> list = new ArrayList<String>();
	    ResultSet rs = null;
	    try {
	        ps = conn.prepareStatement(sql);//sql 
	        rs = ps.executeQuery();//result
	        ResultSetMetaData md = rs.getMetaData();
	        int columnCount = md.getColumnCount();//column number
	        while (rs.next()) {//row
	            for (int i = 1; i <= columnCount; ++i) {
	                list.add(rs.getString(i) == null ? "" : rs.getString(i));
	        }
	    }
	    } catch (SQLException e) {
	        e.printStackTrace();
	    } finally {
	        closeAll(rs, ps, conn);
	    }
	    return list;
	}
	public void getStockName(String ProjName)//get company name in the db //1 function part(1)
	{
		 Connection conn = getConn(ProjName);
	     PreparedStatement ps = null;     
	     ResultSet rs = null;
	     try {
	         DatabaseMetaData md = conn.getMetaData();
	         rs = md.getTables(null, null, "%", null);
	         while (rs.next()) {
	        	 String TableName=rs.getString(3);
	        	 String []stock=TableName.split("_");//goog history
	        	 if(stock[1].equals("realtime"))
	        	 {
	             real_list.add(stock[0]);//goog
	        	 }
	        	 if(stock[1].equals("history"))
	        	 {
	             history_list.add(stock[0]);//goog
	        	 }
	         }
	     } catch (SQLException e) {
	         e.printStackTrace();
	     } finally {
	         closeAll(rs,ps, conn);
	     }
	 }
	private static Connection getConn(String myProjName) {
	    Connection conn = null;
	    try {
	        Class.forName(dbdriver);            
	        String myjdbcUrl = dburl.replace("xinyuDatabaseName", myProjName);
	        conn = DriverManager.getConnection(myjdbcUrl, username, userpassword);
	    } catch (ClassNotFoundException e) {
	        e.printStackTrace();
	    } catch (SQLException e) {
	        e.printStackTrace();
	    }
	    return conn;
	}
	private static void closeAll(ResultSet rs, PreparedStatement ps,
	        Connection conn) {
	    if (rs != null) {
	        try {
	            rs.close();
	        } catch (SQLException e) {
	            e.printStackTrace();
	        }
	    }
	    if (ps != null) {
	        try {
	            ps.close();
	        } catch (SQLException e) {
	            e.printStackTrace();
	        }
	    }
	    if (conn == null)
	        return;
	    try {
	        conn.close();
	    } catch (SQLException e) {
	        e.printStackTrace();
	    }
	}
		    public void readcsv(String path)
			{
			    File csv = new File(path);  // 
			    BufferedReader br = null;
			    try
			    {
			        br = new BufferedReader(new FileReader(csv));
			    } catch (FileNotFoundException e)
			    {
			        e.printStackTrace();
			    }
			    String line = "";
			    String everyLine = "";
			    try {
			           // List<String> allString = new ArrayList<>();
			            while ((line = br.readLine()) != null)  
			            {
			                everyLine = line;
			               // System.out.println(everyLine);
			                indicator.add(everyLine);
			            }
			    } catch (IOException e)
			    {
			        e.printStackTrace();
			    }

			}
		    public  void excutepy(String path) throws IOException,InterruptedException
			 {
				    String exe = "python";
			        String command = path;
			        String[] cmdArr = new String[] {exe,command};
			        Process process = Runtime.getRuntime().exec(cmdArr);
			        InputStream is = process.getInputStream();
			        DataInputStream dis = new DataInputStream(is);
			        String str=dis.readLine();
			        process.waitFor();
			        System.out.println(str);
			 }
	}


