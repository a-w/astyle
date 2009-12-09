// Example2.cpp

/* This program calls the Artistic Style GUI formatter (AStyleMain)
 * to format the astyle source files in a test-c directory.
 */

#include "AStyleInterface.h"

#include <stdlib.h>
#include <string.h>
#include <fstream>
#include <iostream>
using namespace std;

#define FPS 30          // file path size

// function declarations
void error(const char *why, const char* what = "");
char* getText(const char* fileName);
void  setText(const char* textOut, const char* fileName);
void setOptionValues(AStyleInterface& as);


int main(int, char **)
{
    // options to pass to AStyle
    char fileName[][FPS] = { "../test-c/ASBeautifier.cpp",
                             "../test-c/ASFormatter.cpp" ,
                             "../test-c/astyle.h"
                           };
    size_t arraySize = sizeof(fileName) / sizeof(fileName[0]);

    // create an object
    AStyleInterface astyle;

    // set test values for the options
    astyle.setTestOptions();

    // get Artistic Style version
    char* version = AStyleGetVersion();
    cout << "\nArtistic Style " << version << endl;

    // process the input files
    for (size_t i = 0; i < arraySize; i++) {
        // get the text to format
        char* textIn = getText(fileName[i]);

        // call the Artistic Style formatting function
        char* textOut = astyle.formatSource(textIn, fileName[i]);

        // NULL pointer is an error - restore the original file
        // an error message has been displayed by the error handler
        if (textOut == NULL) {
            cout << "cannot format " << fileName[i] << endl;
            return 0;
        }

        // return the formatted text
        cout << "formatted " << fileName[i] << endl;
        setText(textOut, fileName[i]);

        // must delete the temporary buffers
        delete [] textIn;
        delete [] textOut;
    }
#ifdef __MINGW32__
    system("pause");
#endif
}


// Error message function for this example
void error(const char *why, const char* what)
{
    cout << why << ' ' << what << endl;
    cout << "The program has terminated!" << endl;
    exit(1);
}

// get the text to be formatted
// usually the text would be obtained from an edit control
char* getText(const char* fileName)
{
    // open input file
    ifstream in(fileName);
    if (!in)
        error("Could not open input file", fileName);

    // get length of buffer
    in.seekg(0, ifstream::end);
    size_t bufferSizeIn = static_cast<size_t>(in.tellg());
    in.seekg(0, ifstream::beg);

    // allocate memory
    char* bufferIn = new(nothrow) char [bufferSizeIn];
    if (bufferIn == NULL) {
        in.close();
        error("Memory allocation failure on input");
    }

    // read data as a block
    in.read(bufferIn, bufferSizeIn);
    in.close();

    // get actual size - will be smaller than buffer size
    size_t textSizeIn = static_cast<size_t>(in.gcount());
    bufferIn[textSizeIn-1] = '\0';

    return bufferIn;
}

// return the formatted text
// usually the text would be returned to a GUI
void setText(const char* bufferOut, const char* fileName)
{
    // create a backup file
    char origFileName[FPS+5];
    strcpy(origFileName, fileName);
    strcat(origFileName, ".orig");
    remove(origFileName);              // remove a pre-existing file

    if (rename(fileName, origFileName) < 0)
        error("Could not open input file", fileName);

    // open the output file
    ofstream out(fileName);
    if (!out)
        error("Could not open output file", fileName);

    // write the text
    int textSizeOut = strlen(bufferOut);
    out.write(bufferOut, textSizeOut);
    out.close();
}
