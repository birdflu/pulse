package main

// Inverse Fourier transform

// go get -v -u gonum.org/v1/gonum/dsp/fourier

import (
	"gonum.org/v1/gonum/dsp/fourier"
	"fmt"
	"bufio"
    "os"
    "strconv"
)

func sum(array []float64) float64 {  
 result := 0.0  
 for _, v := range array {  
  result += v  
 }  
 return result  
} 

func approximate(yy []float64) []float64 {
	ncnt := len(yy)
	fft := fourier.NewFFT(ncnt)
	freq := fft.Coefficients(nil, yy)
	for i := 0; i < len(freq); i++ {
		if i > 15 { 
			freq[i] = 0
		}
	}
	yyy := fft.Sequence(nil, freq)
	for i := 0; i < ncnt; i++ {
		yyy[i] = yyy[i]/float64(ncnt)
	}
	return yyy
}


func main() {
    file, err := os.Open("spectrum.csv")
    if err != nil {
        fmt.Println(err)
    }
    defer file.Close()

 	var lines []string
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        lines = append(lines, scanner.Text())
    }
    
    var floats []float64
    for i := 0; i < 11947; i++ {
		feetFloat, _ := strconv.ParseFloat(lines[i], 64)
		floats = append(floats, feetFloat)
	}

    result := approximate(floats)

    fmt.Println("Source sum:", sum(floats))
    fmt.Println("Result sum:", sum(result))
}

