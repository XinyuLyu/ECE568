  // written by:Xinyu Lyu
  // assisted by:all team Members
  // debugged by:all team Members
package stock.resource;
import java.io.IOException;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.glassfish.jersey.server.JSONP;

import stock.service.StockService;
import Jama.Matrix;

@Path("stocks")
public class StockResource {
	StockService stockService=new StockService();
	@GET
	@Path("/query/{companyId}")
	//@Path("/{}")
	@JSONP(queryParam=JSONP.DEFAULT_QUERY)
	//@Produces(MediaType.APPLICATION_JSON)
	@Produces("application/x-javascript")
//	public  Response function1(@QueryParam(JSONP.DEFAULT_QUERY) String callback,
//			@PathParam("userId") String userId)
//	{
//		
//		return stockService.getLatestPrice(userId);
//	}
	public  Response function1(@QueryParam(JSONP.DEFAULT_QUERY) String callback,
			@PathParam("companyId") String companyId, @QueryParam("queryId") String queryId)
	{
		if(queryId.equals("query1"))
		{
		return stockService.getLatestPrice("xinyu");
		}else if(queryId.equals("query2"))
		{
		return stockService.getHighestPrice("xinyu",companyId);
		}else if(queryId.equals("query3"))
		{
			return stockService.getAveragePrice("xinyu",companyId);
		}
		else if(queryId.equals("query4"))
		{
			return stockService.getLowestPrice("xinyu",companyId);
		}else if(queryId.equals("query5"))
		{
			return stockService.lesserThanPrice("xinyu",companyId);
		}
		else
		{return null;}
	}
	
	@GET
	@Path("/{userId}/query2/{companyId}")
	@Produces(MediaType.APPLICATION_JSON)
	public  Response function2(@PathParam("userId") String userId,@PathParam("companyId") String companyId)
	{
		return stockService.getHighestPrice(userId,companyId);
	}
	@GET
	@Path("/{userId}/query3/{companyId}")
	@Produces(MediaType.APPLICATION_JSON)
	public  Response function3(@PathParam("userId") String userId,@PathParam("companyId") String companyId)
	{
		return stockService.getAveragePrice(userId,companyId);
	}
	@GET
	@Path("/{userId}/query4/{companyId}")
	@Produces(MediaType.APPLICATION_JSON)
	public  Response function4(@PathParam("userId") String userId,@PathParam("companyId") String companyId)
	{
		return stockService.getLowestPrice(userId,companyId);
	}
	@GET
	@Path("/{userId}/query5/{companyId}")
	@Produces(MediaType.APPLICATION_JSON)
	public  Response function5(@PathParam("userId") String userId,@PathParam("companyId") String companyId)
	{
		return stockService.lesserThanPrice(userId,companyId);
	}
	
	@GET
	@Path("/{userId}/{companyId}/realtime/{minutes}")
	@Produces(MediaType.APPLICATION_JSON)
	public  Response realtime(@PathParam("userId") String userId,@PathParam("companyId") String companyId,@PathParam("minutes") String minutes)
	{
		
		return stockService.realtime(userId,companyId,minutes);
	}
	@GET
	@Path("/{userId}/{companyId}/history/{days}")
	@Produces(MediaType.APPLICATION_JSON)
	public  Response history(@PathParam("userId") String userId,@PathParam("companyId") String companyId,@PathParam("days") String days)
	{
		return stockService.history(userId,companyId,days);
	}
	@GET
	@Path("/getprice/{companyId}")
	@JSONP(queryParam=JSONP.DEFAULT_QUERY)
	@Produces("application/x-javascript")
	public  Response function3(@QueryParam(JSONP.DEFAULT_QUERY) String callback,
			@PathParam("companyId") String companyId, @QueryParam("type") String type,@QueryParam("time") String time) throws IOException, InterruptedException
	{
		if(type.equals("history"))//,@QueryParam("time") String time
		{
			return stockService.history("xinyu",companyId,time);
		}else if(type.equals("realtime"))
		{
			return stockService.realtime("xinyu",companyId,time);
		}
		else
		{return null;}
	}
	@GET
	@Path("/ANN/{companyId}")
	@Produces(MediaType.APPLICATION_JSON)
	public  Response ANN(@PathParam("companyId") String companyId) throws IOException, InterruptedException
	{

		return stockService.ANN(companyId);
	}
	@GET
	@Path("/LSTM/{companyId}")
	@Produces(MediaType.APPLICATION_JSON)
	public  Response LSTM(@PathParam("companyId") String companyId) throws IOException, InterruptedException
	{

		return stockService.LSTM(companyId);
	}
	@GET
	@Path("/SVM/{companyId}")
	@Produces(MediaType.APPLICATION_JSON)
	public  Response SVM(@PathParam("companyId") String companyId) throws IOException, InterruptedException
	{

		return stockService.SVM(companyId);
	}
	@GET
	@Path("/BYS/{companyId}")
	@Produces(MediaType.APPLICATION_JSON)
	public  Response BYS(@PathParam("companyId") String companyId) throws IOException, InterruptedException
	{

		return stockService.BYS(companyId);
	}
	
	@GET
	@Path("/predictor/{companyId}")
	@JSONP(queryParam=JSONP.DEFAULT_QUERY)
	@Produces("application/x-javascript")
	public  Response function2(@QueryParam(JSONP.DEFAULT_QUERY) String callback,
			@PathParam("companyId") String companyId, @QueryParam("preId") String preId) throws IOException, InterruptedException
	{
		if(preId.equals("ANN"))
		{
		return stockService.ANN(companyId);
		}else if(preId.equals("LSTM"))
		{
		return stockService.LSTM(companyId);
		}else if(preId.equals("SVM"))
		{
			return stockService.SVM(companyId);
		}
		else if(preId.equals("BYS"))
		{
			return stockService.BYS(companyId);
		}
		else
		{return null;}
	}
}

