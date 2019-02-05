package stock.model;
import Jama.Matrix;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
//import org.apache.commons.csv.*;
public class  Stock{
	 private static String dbdriver = "com.mysql.jdbc.Driver";
     private static String dburl = "jdbc:mysql://127.0.0.1:3306/xinyuDatabaseName?&useSSL=false";//cmx
     private static String username = "root";
     private static String userpassword = "yfj520520";
     public static Connection conn = null;
public String main(String companyId)// stock name, predict time
//public static void main(String []agrs)
{
	    List<Double>price=GetData("xinyu","SELECT Close_Price FROM goog_History_Price;");
	    Double[] pricet=new Double[price.size()];;
	    price.toArray(pricet);
	    double[] pricetresult = new double[pricet.length];
	    for(int i = 0; i < pricet.length; i++) {
	    	pricetresult[i] = pricet[i].doubleValue();
	    }
		double[] timex=new double [pricet.length];
		for(int i=0;i<timex.length;i++)
		{
			timex[i]=i+1;
		}
		double xt=timex[pricet.length-1]+1;
		return predicted_mean_variance(timex,pricetresult,xt);
		//predicted_mean_variance(timex,pricetresult,xt);
	}
	public static String predicted_mean_variance(double[] x, double[] t,double xt) {// parameters: training x[] traning t[] and test element xt
	int M=3;
	double beta=12;
	double alpha=0.5;
	/*--------------calculate φT(x)-------------------*/
	double [][]a=new double [1][M+1];
	for(int i=0;i<=M;i++)
	{
		a[0][i]=Math.pow(xt,i);
	}
	Matrix Ma=new Matrix(a);
	/*--------------calculate alpha*I-------------------*/
	double [][]arrayI=new double [M+1][M+1];
	for(int i=0;i<M+1;i++)
	{
		for(int j=0;j<M+1;j++)
		{
			if(i==j)arrayI[i][j]=alpha;
		}
	}
	Matrix MI=new Matrix(arrayI);
	/*--------------calculate SUM-φ(xn)-------------------*/
	double [][]b=new double [M+1][1];
		for(int j=0;j<x.length-1;j++)// training data exclude the last element
		{
		   for(int i=0;i<=M;i++)
			{
			b[i][0]+=Math.pow(x[j],i);
			}
		}
		Matrix Mb=new Matrix(b);
  /*------------calculate the matrix S-------------*/		
		Matrix S=Mb.times(Ma).times(beta);
		S=S.plus(MI).inverse();
  /*--------------calculate SUM-[φ(xn)*tn]-------------------*/
		double [][]c=new double [M+1][1];
		for(int j=0;j<x.length-1;j++)// training data exclude the last element
		{
			for(int i=0;i<=M;i++)
			{
			c[i][0]+=Math.pow(x[j],i)*t[j];
			}
		}
		Matrix Mc=new Matrix (c);
		/*--------------calculate mean-------------------*/
		double mean =Ma.times(S).times(Mc).times(beta).get(0,0);
		/*--------------calculate φ(x)-------------------*/
		double [][]d=new double [M+1][1];
		for(int i=0;i<=M;i++)
		{
			d[i][0]=Math.pow(xt,i);
		}
		Matrix Md=new Matrix(d);
		/*--------------calculate variance-------------------*/
		double variance=1/beta+Ma.times(S).times(Md).get(0, 0);
		variance=Math.sqrt(variance);
		//System.out.println("Next Day Value:"+mean);
		return ("NextDayValue "+mean);
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
	private static void closeAll(ResultSet rs, PreparedStatement ps,Connection conn) {
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
	}
	public static List<Double> GetData(String ProjName, String sql)//1 function part(2)
	{
		Connection conn = getConn(ProjName);
	    PreparedStatement ps = null;
	    List<Double> list = new ArrayList<Double>();
	    ResultSet rs = null;
	    try {
	        ps = conn.prepareStatement(sql);//sql 
	        rs = ps.executeQuery();//result
	        ResultSetMetaData md = rs.getMetaData();
	        int columnCount = md.getColumnCount();//column number
	        while (rs.next()) {//row
	            for (int i = 1; i <= columnCount; ++i) {
	                list.add(rs.getDouble(i));//rs.getDouble(i) == null ? "" :
	        }
	    }
	    } catch (SQLException e) {
	        e.printStackTrace();
	    } finally {
	        closeAll(rs, ps, conn);
	    }
	    return list;
	}
}