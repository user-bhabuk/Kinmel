package Coursework;

public class Retailer extends Store 
{
    //using the concept of encapsulation to not let the attribute be accessed directly
    private int VATInclusivePrice;
    private int loyaltyPoint;
    private boolean isPaymentOnline;
    private String purchasedYear;
    private int storeId;

    public Retailer(int storeId, String storeName, String location, 
                    String openingHour,double totalSales, double totalDiscount
                    ,int VATInclusivePrice, boolean isPaymentOnline, 
                    String purchasedYear)
    {
        //Calling constructor
        super(storeId, storeName, location, openingHour);
        setTotalSales(totalSales);
        setTotalDiscount(totalDiscount);
        this.VATInclusivePrice = VATInclusivePrice;
        this.isPaymentOnline = isPaymentOnline;
        this.purchasedYear = purchasedYear;
        this.loyaltyPoint = 0;
    }

    public int getStoreId() {
        return storeId;
    }
    //accessor/getter method
    public int getVATInclusivePrice() 
    {
        return VATInclusivePrice;
    }
    //setter method
    public void setVATInclusivePrice(int VATInclusivePrice) 
    {
        this.VATInclusivePrice = VATInclusivePrice;
    }
    //accessor/getter method
    public int getLoyaltyPoint()
    {
        return loyaltyPoint;
    }
    //setter method
    public void setLoyaltyPoint(int loyaltyPoint)
    {
        this.loyaltyPoint = loyaltyPoint;
    }
    //accessor/getter method
    public boolean isPaymentOnline() 
    {
        return isPaymentOnline;
    }
    //setter method
    public void setIsPaymentOnline(boolean isPaymentOnline) 
    {
        this.isPaymentOnline = isPaymentOnline;
    }
    //accessor/getter method
    public String getPurchasedYear() 
    {
        return purchasedYear;
    }
    //setter method
    public void setPurchasedYear(String purchasedYear) 
    {
        this.purchasedYear = purchasedYear;
    }
    //setter method
    public void setLoyaltyPoint(boolean isOnline, int VATPrice) 
    {
        if (isOnline) {
            setLoyaltyPoint((int) (VATPrice * 0.01));

        }
    }
    //This method removes a product if it has no loyalty points
    public void removeProduct()
    {
        if (getLoyaltyPoint() == 0 && (getPurchasedYear().equals("2020") || getPurchasedYear().equals("2021") || getPurchasedYear().equals("2022"))) 
        {
            setVATInclusivePrice(0);
            setLoyaltyPoint(0);
            setIsPaymentOnline(false);
        }
        else{
            System.out.println("");
        }
    }
    //Displaying the details of the Retailer class 
    public void display() 
    {
        super.display();
        if (getVATInclusivePrice() != 0 || getLoyaltyPoint() != 0 || isPaymentOnline()) 
        {
            System.out.println("The VAT Inclusive Price: " + getVATInclusivePrice());
            System.out.println("The Loyalty Point is: " + getLoyaltyPoint());
            System.out.println("The Purchased Year is: " + getPurchasedYear());
        }
        else
        {
            System.out.println("The Product has been removed.");
        }
    }

    public String getMarkedPrice() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getMarkedPrice'");
    }

    public String getSellingPrice() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getSellingPrice'");
    }

    public String getProductName() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getProductName'");
    }

    public void setLoyaltyPoints(double vatPrice) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'setLoyaltyPoints'");
    }

    public void updateloyaltyPanel(boolean isInSales, double vATpriceDouble) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'updateloyaltyPanel'");
    }

    void setLoyaltypoint(boolean inSales, double VATpriceDouble) {
        throw new UnsupportedOperationException("Not supported yet.");
    }
}