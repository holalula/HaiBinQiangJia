#define _CRT_SECURE_NO_WARNINGS
#pragma once

#include <iostream>
#include <string>

#include <Windows.h>
#include <TlHelp32.h>


// Better than using namespace std;

using std::cout;
using std::endl;
using std::string;

// datatype for a module in memory (dll, regular exe) 
struct module
{
	SIZE_T dwBase, dwSize;
};

class SignatureScanner
{
public:
    module TargetModule;  // Hold target module
	HANDLE TargetProcess; // for target process
	SIZE_T  TargetId;      // for target process

	// For getting a handle to a process
	HANDLE GetProcess(char* processName)
	{
		HANDLE handle = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, NULL);
		PROCESSENTRY32 entry;
		entry.dwSize = sizeof(entry);

		do{
			char output[512];
			sprintf_s(output, "%ws", entry.szExeFile);
			if (!strcmp(output, processName)) {
				TargetId = entry.th32ProcessID;
				CloseHandle(handle);
				TargetProcess = OpenProcess(PROCESS_ALL_ACCESS, false, TargetId);
				return TargetProcess;
			}
		}
		while (Process32Next(handle, &entry));

		cout <<"Error:"<<GetLastError() << endl;
		return NULL;
	}

	// For getting information about the executing module
	module GetModule(char* moduleName) {
		HANDLE hmodule = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, TargetId);
		MODULEENTRY32 mEntry;
		mEntry.dwSize = sizeof(mEntry);

		do {
			char output[512];
			sprintf_s(output, "%ws", mEntry.szModule);
			if (!strcmp(output, (LPSTR)moduleName)) {
				CloseHandle(hmodule);

				TargetModule = { (SIZE_T)mEntry.hModule, mEntry.modBaseSize };
				return TargetModule;
			}
		} while (Module32Next(hmodule, &mEntry));

		module mod = { (SIZE_T)false, (SIZE_T)false };
		return mod;
	}

	// Basic WPM wrapper, easier to use.
	template <typename var>
	bool WriteMemory(SIZE_T Address, var Value) {
		return WriteProcessMemory(TargetProcess, (LPVOID)Address, &Value, sizeof(var), 0);
	}

	// Basic RPM wrapper, easier to use.
	template <typename var>
	var ReadMemory(SIZE_T Address) {
		var value;
		ReadProcessMemory(TargetProcess, (LPCVOID)Address, &value, sizeof(var), NULL);
		return value;
	}

	// for comparing a region in memory, needed in finding a signature
	bool MemoryCompare(const BYTE* bData, const BYTE* bMask, const char* szMask) {
		for (; *szMask; ++szMask, ++bData, ++bMask) {
			if (*szMask == 'x' && *bData != *bMask) {
				return false;
			}
		}
		return (*szMask == NULL);
	}

	// for finding a signature/pattern in memory of another process
	SIZE_T FindSignature(SIZE_T start, SIZE_T size, const char* sig, const char* mask)
	{
		BYTE* data = new BYTE[size];
		SIZE_T bytesRead;

		ReadProcessMemory(TargetProcess, (LPVOID)start, data, size, &bytesRead);
		for (SIZE_T i = 0; i < size; i++)
		{
			if (MemoryCompare((const BYTE*)(data + i), (const BYTE*)sig, mask)) {
				return start + i;
			}
		}
		delete[] data;
		return NULL;
	}
};