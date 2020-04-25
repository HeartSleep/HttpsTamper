package main
 
import (
	"fmt"
	"time"
)
 
func main(){
	for i:=0;i<100;i++{
		fmt.Println("Hello ARM")
		time.Sleep(time.Second)
		fmt.Println(time.Now())
	}
 
}