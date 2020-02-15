package main

import (
	"fmt"
	"time"
)

func simpleswith() {
	i := 2
	fmt.Print("write ", i, " as ")
	switch i {
	case 1:
		fmt.Println("one")
	case 2:
		fmt.Println("two")
	case 3:
		fmt.Println("three")
	}
}

func switchtimeweekday() {
	switch time.Now().Weekday() {
	case time.Saturday, time.Sunday:
		fmt.Println("it's the weekend")
	default:
		fmt.Println("it's a weekday")
	}
}

func beforenoon() {
	t := time.Now()
	switch {
	case t.Hour() < 12:
		fmt.Println("it's before noon")
	default:
		fmt.Println("it's after noon")
	}
}

func callfunc() {
	whatAmI := func(i interface{}) string {
		switch t := i.(type) {
		case bool:
			return "I am a bool"
		case int:
			return "I am an int"
		default:
			return fmt.Sprintf("Can't handle type %T", t)
		}
	}
	fmt.Println(whatAmI(1))
	fmt.Println(whatAmI(true))
	fmt.Println(whatAmI("hey"))
}

func main() {
    var a [5]int
	fmt.Println("emp:", a)
	
	a[4] = 100
    fmt.Println("set:", a)
	fmt.Println("get:", a[4])
	
	fmt.Println("len:", len(a))

	b := [5]int{1, 2, 3, 4, 5}
	fmt.Println("dcl:", b)

    var twoD [2][3]int
    for i := 0; i < 2; i++ {
        for j := 0; j < 3; j++ {
            twoD[i][j] = i + j
        }
    }
    fmt.Println("2d: ", twoD)

}
