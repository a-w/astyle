#ifndef ASTYLE_TESTCON_H
#define ASTYLE_TESTCON_H

// AStyleTestCon tests the ASConsole class only. This class is used only in
// the console build. It also tests the parseOption function for options used
// by only by the console build (e.g. recursive, preserve-date, verbose). It
// does not explicitely test the ASStreamIterator class or any other part
// of the program.

//-------------------------------------------------------------------------
// headers
//-------------------------------------------------------------------------

#include <UnitTest++.h>
#include <stdlib.h>
#include <vector>
#include <iostream>  // for cout
#include <fstream>
#include <errno.h>
using namespace std;
#include "astyle_main.h"
using namespace astyle;

//-------------------------------------------------------------------------
// extern global variables in astyle_main.cpp
//-------------------------------------------------------------------------

// global variables in astyle_main.cpp
namespace astyle
{
extern ASConsole* g_console;
extern ostream* _err;
}

//-------------------------------------------------------------------------
// declarations
//-------------------------------------------------------------------------

// functions in AStyleTestCon_Main.cpp
char** buildArgv(const vector<string>& argIn);
int buildFileNameVector(string fileToProcess, vector<string>& fileNameVector);
void cleanTestDirectory(const string &directory);
void createConsoleGlobalObject(ASFormatter& formatter);
void createTestDirectory(const string &dirName);
void createTestFile(const string& testFilePath, const char* testFileText, int size = 0);
void deleteConsoleGlobalObject();
string getCurrentDirectory();
string getTestDirectory();
void removeTestDirectory();
void removeTestFile(const string& testFileName);
void systemPause(const string& message);
bool writeOptionsFile(const string& optionsFileName, const char* fileIn);

//-------------------------------------------------------------------------

#endif // closes ASTYLE_TESTCON_H
