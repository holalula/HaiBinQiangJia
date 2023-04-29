#pragma once
#include <vector>
struct FurnitureInstance {
	int category;
	int color;
	float x, y, z, r;
	FurnitureInstance(int c, float x, float y, float z, float r, int color) :category(c), x(x), y(y), z(z), r(r), color(color) {}
};
struct CategoryInstance {
	CategoryInstance(int categoryId) { this->categoryId = categoryId; this->count = 0; this->_p = 0; };
	CategoryInstance() {};
	int categoryId;
	int count;
	std::vector<float> posX;
	std::vector<float> posY;
	std::vector<float> posZ;
	std::vector<float> r;
	std::vector<int> color;
	int _p = 0;
};