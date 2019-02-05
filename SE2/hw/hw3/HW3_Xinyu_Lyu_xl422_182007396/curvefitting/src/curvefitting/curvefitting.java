package curvefitting;

import Jama.Matrix;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import org.apache.commons.csv.*;
public class curvefitting {
public static void main(String []agrs)
{
	String[] files= {"CCF-03-02-2017","CCF-hist-2016-2017","FB-03-02-2017","FB-hist-2016-2017","GOOG-03-02-2017","GOOG-hist-2016-2017","MSFT-03-02-2017","MSFT-hist-2016-2017","YHOO-03-02-2017","YHOO-hist-2016-2017"};
	for(int i=0;i<files.length;i++) {
		System.out.println("Predicted RESULT for "+files[i]+":");
		double[][] data=readData(files[i]);
		double[] timex=data[0];                   //time data
		double[] pricet=data[1];                 // price data
		double xt=timex[timex.length-1];          // test data is the last time element in the time data
	    predicted_mean_variance(timex,pricet,xt);
		}
	}
	public static void predicted_mean_variance(double[] x, double[] t,double xt) {// parameters: training x[] traning t[] and test element xt
	int M=4;
	double beta=12;
	double alpha=0.1;
	/*--------------calculate ¦ÕT(x)-------------------*/
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
	/*--------------calculate SUM-¦Õ(xn)-------------------*/
	double [][]b=new double [M+1][1];
		for(int j=0;j<x.length-1;j++)
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
  /*--------------calculate SUM-[¦Õ(xn)*tn]-------------------*/
		double [][]c=new double [M+1][1];
		for(int j=0;j<x.length-1;j++)
		{
			for(int i=0;i<=M;i++)
			{
			c[i][0]+=Math.pow(x[j],i)*t[j];
			}
		}
		Matrix Mc=new Matrix (c);
		/*--------------calculate mean-------------------*/
		double mean =Ma.times(S).times(Mc).times(beta).get(0,0);
		/*--------------calculate ¦Õ(x)-------------------*/
		double [][]d=new double [M+1][1];
		for(int i=0;i<=M;i++)
		{
			d[i][0]=Math.pow(xt,i);
		}
		Matrix Md=new Matrix(d);
		/*--------------calculate variance-------------------*/
		double variance=1/beta+Ma.times(S).times(Md).get(0, 0);
		variance=Math.sqrt(variance);
		/*--------------print-------------------*/
	    System.out.println("Predicted price is: "+mean);
	    System.out.println("True value is: "+t[t.length-1]);
 	    System.out.println("More precisely estimation: ["+(mean-3*variance)+","+(mean+3*variance)+"]");
        System.out.println("The absolute error for mean is: "+ Math.abs(t[t.length-1]-mean));	
        System.out.println("The relative error for mean is: "+(Math.abs((t[t.length-1]-mean)/t[t.length-1]))*100+"%");
        System.out.println();
	}
	public static double[][] readData(String fileName) {//cited from https://github.com/MrHohn/StockPricePrediction
		                                                // read data from .csv
		
		// read CSV data into array
		double[] xArr=new double[1000];
		double[] tArr=new double[1000];
		Reader in = null;
		
		try {
			in=new FileReader(fileName+".csv");
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		Iterable<CSVRecord> records=null;
		try {
			records=CSVFormat.EXCEL.parse(in);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		int index=0;
		for(CSVRecord record:records) {
			xArr[index]=Double.valueOf(record.get(0));
			tArr[index]=Double.valueOf(record.get(1));
			index++;
		}
		;
		double[][] result=new double[2][index];
		System.arraycopy(xArr, 0, result[0], 0, index);
		System.arraycopy(tArr, 0, result[1], 0, index);
		return result;
	}
}