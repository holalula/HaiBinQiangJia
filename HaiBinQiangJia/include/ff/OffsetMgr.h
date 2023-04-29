#ifndef __OFFSETMGR_H
#define __OFFSETMGR_H
#pragma once
#include "../../pch.h"
#include <vector>

static class DLLAPI OffsetMgr {
public:
	
	static std::vector<SIZE_T> ActiveItemPosition2;
	static std::vector<SIZE_T> ActiveItemRotation2;

	static SIZE_T IsWarehouseOffset;


	//Boogiepop
	static __int64 offset_OperateItem;
	static __int64 offset_Loadhouse;
	static __int64 offset_ViewMatrix;
	static __int64 offset_Select;
	//using
	static SIZE_T pa1Offset;
	static SIZE_T pa2Offset;
	static SIZE_T pa3Offset;
	static SIZE_T blueOffset;

	static std::vector<SIZE_T> ActiveItemState1_hoverORmoverotate; //ACTIVE NOTHING:0 HOVER:1 MOVE/ROTATE:3
	static std::vector<SIZE_T> ActiveItemState2_moveORrotate; //MOVE:1 or ROTATE:2

	static std::vector<SIZE_T> SJPosition;
	static std::vector<SIZE_T> SJRotation;
	static std::vector<SIZE_T> SJPositionX;
	static std::vector<SIZE_T> SJPositionY;
	static std::vector<SIZE_T> SJPositionZ;

	static std::vector<SIZE_T> IsRotating;
	static std::vector<SIZE_T> IsRotating2;

	static SIZE_T baseHouse;

	static __int64 offset_SavePreview;

	static SIZE_T ActortableBase;
	static std::vector<SIZE_T> ActorName;
	static std::vector<SIZE_T> ActorHomeworld;
	static std::vector<SIZE_T> ActorId;

	static std::vector<SIZE_T> Furniture_List;

	static SIZE_T layoutWorld;
};
SIZE_T OffsetMgr::IsWarehouseOffset = 0x08 - 0x10;

/*PA1:
Address of signature = ffxiv_dx11.exe + 0x00576E5A
"\xC6\x87\x73\x01\x00\x00\x00\x4D\x8B", "xxxxxx?xx"
"C6 87 73 01 00 00 ? 4D 8B"

PA2:
Address of signature = ffxiv_dx11.exe + 0x00577911
"\xC6\x87\x73\x01\x00\x00\x00\x80\xBF\x73\x01\x00\x00", "xxxxxx?xxxxxx"
"C6 87 73 01 00 00 ? 80 BF 73 01 00 00"

BLUE:
Address of signature = ffxiv_dx11.exe + 0x005731C0
"\x48\x85\x00\x0F\x84\x00\x00\x00\x00\x48\x89\x00\x00\x00\x57\x48\x83\xEC\x00\x48\x8B\x00\x48\x8B\x00\xE8\x00\x00\x00\x00\x33\xD2", "xx?xx????xx???xxxx?xx?xx?x????xx"
"48 85 ? 0F 84 ? ? ? ? 48 89 ? ? ? 57 48 83 EC ? 48 8B ? 48 8B ? E8 ? ? ? ? 33 D2"

OperateItem：
Address of signature = ffxiv_dx11.exe + 0x005732C9
"\x48\x89\x00\x00\x00\x57\x48\x83\xEC\x00\x48\x8B\x00\x48\x8B\x00\xE8\x00\x00\x00\x00\x8B\x07", "xx???xxxx?xx?xx?x????xx"
"48 89 ? ? ? 57 48 83 EC ? 48 8B ? 48 8B ? E8 ? ? ? ? 8B 07"

loadhouse：
Address of signature = ffxiv_dx11.exe + 0x00B50D70
"\x48\x8B\x00\x00\x48\x85\x00\x74\x00\x48\x8D\x00\x00\xE9", "xx??xx?x?xx??x"
"48 8B ? ? 48 85 ? 74 ? 48 8D ? ? E9"

viewmatrix：
Address of signature = ffxiv_dx11.exe + 0x003DC920
"\x40\x00\x48\x83\xEC\x00\x65\x48\x00\x00\x00\x00\x00\x00\x00\x8B\x0D\x00\x00\x00\x00\xBA\x00\x00\x00\x00\x48\x8B\x00\x00\x8B\x04\x00\x39\x05\x00\x00\x00\x00\x7F\x00\x48\x8D\x00\x00\x00\x00\x00\x48\x83\xC4\x00\x5B\xC3\x48\x8D\x00\x00\x00\x00\x00\xE8\x00\x00\x00\x00\x83\x3D\xEF\x24\x9A\x01", "x?xxx?xx???????xx????x????xx??xx?xx????x?xx?????xxx?xxxx?????x????xxxxxx"
"40 ? 48 83 EC ? 65 48 ? ? ? ? ? ? ? 8B 0D ? ? ? ? BA ? ? ? ? 48 8B ? ? 8B 04 ? 39 05 ? ? ? ? 7F ? 48 8D ? ? ? ? ? 48 83 C4 ? 5B C3 48 8D ? ? ? ? ? E8 ? ? ? ? 83 3D EF 24 9A 01"*/
/*
* baseHouse:
* Address of signature = ffxiv_dx11.exe + 0x00559ADD
ffxiv_dx11.exe+559ADD - 48 8B 0D 74F48201     - mov rcx,[ffxiv_dx11.exe+1D88F58] { (1CB27BBB2D0) }
"\x48\x8B\x00\x00\x00\x00\x00\x48\x85\x00\x74\x00\x48\x8B\x00\x00\xE9\x00\x00\x00\x00\xC3\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC", "xx?????xx?x?xx??x????xxxxxxxxxxxx"
"48 8B ? ? ? ? ? 48 85 ? 74 ? 48 8B ? ? E9 ? ? ? ? C3 CC CC CC CC CC CC CC CC CC CC CC"
*/

SIZE_T OffsetMgr::pa1Offset = 0;//0x576E5A;
SIZE_T OffsetMgr::pa2Offset = 0;//0x577911;
SIZE_T OffsetMgr::pa3Offset = 0;//0x577911;
SIZE_T OffsetMgr::blueOffset = 0;//0x5731c0;
__int64 OffsetMgr::offset_OperateItem = 0;//0x5732C9;
__int64 OffsetMgr::offset_Loadhouse = 0;//0xB50D70;
__int64 OffsetMgr::offset_ViewMatrix = 0;//0x3dc920;
__int64 OffsetMgr::offset_SavePreview = 0;//0x572b60
__int64 OffsetMgr::offset_Select = 0;
/*
* Another:
* OperateItem:0x5732C9
* Address of signature = ffxiv_dx11.exe + 0x005732CE
"\x57\x48\x83\xEC\x00\x48\x8B\x00\x48\x8B\x00\xE8\x00\x00\x00\x00\x8B\x07", "xxxx?xx?xx?x????xx"
"57 48 83 EC ? 48 8B ? 48 8B ? E8 ? ? ? ? 8B 07"
LoadHouse:0xB50D70
Address of signature = ffxiv_dx11.exe + 0x00B50D75
"\x85\xC0\x74\x00\x48\x8D\x00\x00\xE9\x00\x00\x00\x00\x48\x8B", "xxx?xx??x????xx"
"85 C0 74 ? 48 8D ? ? E9 ? ? ? ? 48 8B"
offset_ViewMatrix:0x3dc920
Address of signature = ffxiv_dx11.exe + 0x003DC925
"\x20\x65\x00\x8B\x04\x00\x00\x00\x00\x00\x8B\x0D\x00\x00\x00\x00\xBA\x00\x00\x00\x00\x48\x8B\x00\x00\x8B\x04\x00\x39\x05\x00\x00\x00\x00\x7F\x00\x48\x8D\x00\x00\x00\x00\x00\x48\x83\xC4\x00\x5B\xC3\x48\x8D\x00\x00\x00\x00\x00\xE8\x00\x00\x00\x00\x83\x3D\xEF\x24\x9A\x01", "xx?xx?????xx????x????xx??xx?xx????x?xx?????xxx?xxxx?????x????xxxxxx"
"20 65 ? 8B 04 ? ? ? ? ? 8B 0D ? ? ? ? BA ? ? ? ? 48 8B ? ? 8B 04 ? 39 05 ? ? ? ? 7F ? 48 8D ? ? ? ? ? 48 83 C4 ? 5B C3 48 8D ? ? ? ? ? E8 ? ? ? ? 83 3D EF 24 9A 01"
*/

/*
* 5.55 viewmatrix
* Address of signature = ffxiv_dx11.exe + 0x003E08C5
"\x20\x65\x00\x8B\x04\x00\x00\x00\x00\x00\x8B\x0D\x00\x00\x00\x00\xBA\x00\x00\x00\x00\x48\x8B\x00\x00\x8B\x04\x00\x39\x05\x00\x00\x00\x00\x7F\x00\x48\x8D\x00\x00\x00\x00\x00\x48\x83\xC4\x00\x5B\xC3\x48\x8D\x00\x00\x00\x00\x00\xE8\x00\x00\x00\x00\x83\x3D\xCF\x25\x9D\x01", "xx?xx?????xx????x????xx??xx?xx????x?xx?????xxx?xxxx?????x????xxxxxx"
"20 65 ? 8B 04 ? ? ? ? ? 8B 0D ? ? ? ? BA ? ? ? ? 48 8B ? ? 8B 04 ? 39 05 ? ? ? ? 7F ? 48 8D ? ? ? ? ? 48 83 C4 ? 5B C3 48 8D ? ? ? ? ? E8 ? ? ? ? 83 3D CF 25 9D 01"
*/
/*
* PaoChe viewmatrix
* Address of signature = ffxiv_dx11.exe + 0x003E08B5
"\x20\x65\x00\x8B\x04\x00\x00\x00\x00\x00\x8B\x0D\x00\x00\x00\x00\xBA\x00\x00\x00\x00\x48\x8B\x00\x00\x8B\x04\x00\x39\x05\x00\x00\x00\x00\x7F\x00\x48\x8D\x00\x00\x00\x00\x00\x48\x83\xC4\x00\x5B\xC3\x48\x8D\x00\x00\x00\x00\x00\xE8\x00\x00\x00\x00\x83\x3D\xDF\x75\x9C\x01", "xx?xx?????xx????x????xx??xx?xx????x?xx?????xxx?xxxx?????x????xxxxxx"
"20 65 ? 8B 04 ? ? ? ? ? 8B 0D ? ? ? ? BA ? ? ? ? 48 8B ? ? 8B 04 ? 39 05 ? ? ? ? 7F ? 48 8D ? ? ? ? ? 48 83 C4 ? 5B C3 48 8D ? ? ? ? ? E8 ? ? ? ? 83 3D DF 75 9C 01"
*/

/*
* 6.05
Address of signature = ffxiv_dx11.exe + 0x003EED55
"\x20\x65\x00\x8B\x04\x00\x00\x00\x00\x00\x8B\x0D\x00\x00\x00\x00\xBA\x00\x00\x00\x00\x48\x8B\x00\x00\x8B\x04\x00\x39\x05\x00\x00\x00\x00\x7F\x00\x48\x8D\x00\x00\x00\x00\x00\x48\x83\xC4\x00\x5B\xC3\x48\x8D\x00\x00\x00\x00\x00\xE8\x00\x00\x00\x00\x83\x3D\x3F\xD0\xA7\x01", "xx?xx?????xx????x????xx??xx?xx????x?xx?????xxx?xxxx?????x????xxxxxx"
"20 65 ? 8B 04 ? ? ? ? ? 8B 0D ? ? ? ? BA ? ? ? ? 48 8B ? ? 8B 04 ? 39 05 ? ? ? ? 7F ? 48 8D ? ? ? ? ? 48 83 C4 ? 5B C3 48 8D ? ? ? ? ? E8 ? ? ? ? 83 3D 3F D0 A7 01"
*/

/*SavePreview  0x572b60
* Address of signature = ffxiv_dx11.exe + 0x00572B65
"\x48\x89\x00\x00\x00\x48\x89\x00\x00\x00\x55\x48\x8D\x00\x00\x00\x48\x81\xEC\x00\x00\x00\x00\x48\x8B\x00\x00\x00\x00\x00\x48\x33\x00\x48\x89\x00\x00\x0F\x10", "xx???xx???xxx???xxx????xx?????xx?xx??xx"
"48 89 ? ? ? 48 89 ? ? ? 55 48 8D ? ? ? 48 81 EC ? ? ? ? 48 8B ? ? ? ? ? 48 33 ? 48 89 ? ? 0F 10"
*/
//this.matrixSingletonAddress = this.pi.TargetModuleScanner.ScanText("E8 ?? ?? ?? ?? 48 8D 4C 24 ?? 48 89 4c 24 ?? 4C 8D 4D ?? 4C 8D 44 24 ??");
/*
* baseHouse:
* Address of signature = ffxiv_dx11.exe + 0x00559ADD
ffxiv_dx11.exe+559ADD - 48 8B 0D 74F48201     - mov rcx,[ffxiv_dx11.exe+1D88F58] { (1CB27BBB2D0) }
"\x48\x8B\x00\x00\x00\x00\x00\x48\x85\x00\x74\x00\x48\x8B\x00\x00\xE9\x00\x00\x00\x00\xC3\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC", "xx?????xx?x?xx??x????xxxxxxxxxxxx"
"48 8B ? ? ? ? ? 48 85 ? 74 ? 48 8B ? ? E9 ? ? ? ? C3 CC CC CC CC CC CC CC CC CC CC CC"
*/
//ffxiv_dx11.exe+55EA6D - 48 8B 0D 14F48501     - mov rcx,[ffxiv_dx11.exe+1DBDE88] { (2A5E26BB020) }

//SIZE_T OffsetMgr::baseHouse = 0x01D88F58; //mov里面的，可能会变化
//SIZE_T OffsetMgr::baseHouse = 0x1db2e88;//5.5x //0x1DBDE88; //5.55
//SIZE_T OffsetMgr::baseHouse = 0x1db1e88;//5.5x //0x1DBDE88; //5.55
SIZE_T OffsetMgr::baseHouse = 0x2056C88;//0x204FF88 //0X2058E88;//0x1f65d30;//0x1e76db0;//6.05
std::vector<SIZE_T> OffsetMgr::ActiveItemPosition2{ OffsetMgr::baseHouse,0x40,0x80,0x110 };  //5.4 01D89F58
std::vector<SIZE_T> OffsetMgr::ActiveItemRotation2{ OffsetMgr::baseHouse,0x40,0x80,0x124 }; //5.31 01D09A88
std::vector<SIZE_T> OffsetMgr::ActiveItemState1_hoverORmoverotate{ OffsetMgr::baseHouse, 0x40, 0x8 }; //ACTIVE NOTHING:0 HOVER:1 MOVE/ROTATE:3
std::vector<SIZE_T> OffsetMgr::ActiveItemState2_moveORrotate{ OffsetMgr::baseHouse, 0x40, 0x0 }; //MOVE:1 or ROTATE:2
std::vector<SIZE_T> OffsetMgr::SJPosition{ OffsetMgr::baseHouse, 0x40, 0x18, 0x50 };
std::vector<SIZE_T> OffsetMgr::SJRotation{ OffsetMgr::baseHouse, 0x40, 0x18, 0x60 };
std::vector<SIZE_T> OffsetMgr::IsRotating{ OffsetMgr::baseHouse, 0x40, 0xb8 };
std::vector<SIZE_T> OffsetMgr::IsRotating2{ OffsetMgr::baseHouse, 0x40, 0x90 };

std::vector<SIZE_T> OffsetMgr::SJPositionX{ OffsetMgr::baseHouse, 0x40, 0x18, 0x50 };
std::vector<SIZE_T> OffsetMgr::SJPositionY{ OffsetMgr::baseHouse, 0x40, 0x18, 0x50 +0x4};
std::vector<SIZE_T> OffsetMgr::SJPositionZ{ OffsetMgr::baseHouse, 0x40, 0x18, 0x50 +0x8};

//BDTH
//housingModulePtr = Plugin.TargetModuleScanner.GetStaticAddressFromSig("40 53 48 83 EC 20 33 DB 48 39 1D ?? ?? ?? ?? 75 2C 45 33 C0 33 D2 B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? 48 85 C0 74 11 48 8B C8 E8 ?? ?? ?? ?? 48 89 05 ?? ?? ?? ?? EB 07", 0xA);
std::vector<SIZE_T> OffsetMgr::Furniture_List{ 0x209E130 , 0x10, 0x8980 };//0x2097430 //0x20a0330 //TODO: remove hardcode 6.2:20a0330 old:0x1fac070
/*
* //this.ActorTable = sig.GetStaticAddressFromSig("48 8D 0D ?? ?? ?? ?? E8 ?? ?? ?? ?? 44 0F B6 83");
* ffxiv_dx11.exe+A8D0B0 - 48 8D 0D D9F33101     - lea rcx,[ffxiv_dx11.exe+1DAC490] { (286BBA57050) }
*/
//SIZE_T OffsetMgr::ActortableBase = 0x1dac490;
//ffxiv_dx11.exe+A997B1 - 48 8D 0D 087B3401     - lea rcx,[ffxiv_dx11.exe+1DE12C0] { (2A5D9F25050) }

SIZE_T OffsetMgr::ActortableBase = 0x207C6A8;//0x20759a8 //0X207E8A8;//0x1F8B6D8;//0x1e9c528;//0x1dd52c0;//0x1DE12C0;
std::vector<SIZE_T> OffsetMgr::ActorName{ OffsetMgr::ActortableBase,0x30 };
std::vector<SIZE_T> OffsetMgr::ActorHomeworld{ OffsetMgr::ActortableBase,0x195E };
std::vector<SIZE_T> OffsetMgr::ActorId{ OffsetMgr::ActortableBase,0x30 };

// layoutWorldPtr("48 8B 0D ?? ?? ?? ?? 48 85 C9 74 ?? 48 8B 49 40 E9 ?? ?? ?? ??", 2);
SIZE_T OffsetMgr::layoutWorld = 0x2056C88;

#endif