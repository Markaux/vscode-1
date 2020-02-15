
package main
import "fmt"
import "math"

const s string = "constante"
const n = 500000000
const d = 3e20 / n

func hellworld(){
	fmt.Println("hello world")
	fmt.Println("Go" + "lang")
    fmt.Println("1+1 =", 1+1)
    fmt.Println("7.0/3.0 =", 7.0/3.0)
	fmt.Println(true && false)
    fmt.Println(true || false)
    fmt.Println(!true)
	
	var a string = "initial"
	var b,c int = 1,2
	var d = true
	var e int
	f := "short"
	fmt.Println(a)
	fmt.Println(b, c)
	fmt.Println(d)
	fmt.Println(e)
	fmt.Println(f)
}

func themath(){
	fmt.Println(s)
	fmt.Println(d)
	fmt.Println(int64(d))
	fmt.Println(math.Sin(n))
	fmt.Println(math.Cos(n))
}

func foronly(){
	i := 1
    for i <= 3 {
        fmt.Println(i)
        i = i + 1
    }

    for j := 7; j <= 9; j++ {
        fmt.Println(j)
    }
	
    for {
        fmt.Println("loop")
        break
    }
}

func ifthenelse(){
    if 7%2 == 0 {
        fmt.Println("7 is even")
    } else {
        fmt.Println("7 is odd")
    }

    if 8%4 == 0 {
        fmt.Println("8 is divisible by 4")
    }

    if num := 9; num < 0 {
        fmt.Println(num, "is negative")
    } else if num < 10 {
        fmt.Println(num, "has 1 digit")
    } else {
        fmt.Println(num, "has multiple digits")
    }	
}

// func main() {
	
// }
