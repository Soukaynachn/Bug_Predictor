public class ComplexCalculation {
    public static void main(String[] args) {
        int result = 0;
        for (int i = 0; i < 100; i++) {
            if (i % 2 == 0) {
                result += i;
            } else {
                result -= i;
            }
        }
        System.out.println("Result: " + result);
        
        if (result > 0) {
            System.out.println("Positive");
        } else if (result < 0) {
            System.out.println("Negative");
        } else {
            System.out.println("Zero");
        }
    }
    
    public int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
}
