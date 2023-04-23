/*
    Ref:
    * https://llvm.org/doxygen/
    * https://llvm.org/docs/GettingStarted.html
    * https://llvm.org/docs/WritingAnLLVMPass.html
    * https://llvm.org/docs/ProgrammersManual.html
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/Type.h"

using namespace llvm;

char LabPass::ID = 0;

bool LabPass::doInitialization(Module &M)
{
    return true;
}

static Constant *createGlobalStrPtr(Module &M, char const *str, Twine const &name)
{
    LLVMContext &ctx = M.getContext();
    // 創建一個常數字串
    Constant *strConstant = ConstantDataArray::getString(ctx, str);
    // 建立全域變數
    GlobalVariable *strGlobal = new GlobalVariable(M, strConstant->getType(), true, GlobalValue::InternalLinkage, strConstant, name);
    // 創建陣列[0, 0], 意指僅選擇陣列的第一格的指標
    Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
    Constant *indices[] = {zero, zero};
    // 回傳指向該全域變數的指標
    return ConstantExpr::getGetElementPtr(Type::getInt8PtrTy(ctx), strGlobal, indices, true);
}

bool LabPass::runOnModule(Module &M)
{
    errs() << "runOnModule\n";

    LLVMContext &ctx = M.getContext();

    Type *type_int = Type::getInt32Ty(ctx);

    // 創建printf函數呼叫
    FunctionType *type_printf = FunctionType::get(type_int, {Type::getInt8PtrTy(ctx)}, true);
    FunctionCallee callee_printf = M.getOrInsertFunction("printf", type_printf);

    // 創建數字常數
    Constant *one = ConstantInt::get(type_int, 1, true);
    Constant *negOne = ConstantInt::get(type_int, -1, true);

    // 創建字串指標常數
    Constant *format = createGlobalStrPtr(M, "%*s%s: %p\n", "format");
    Constant *emptyStr = createGlobalStrPtr(M, "", "emptyStr");

    // 在全域新增變數 depth，紀錄當前運行深度
    GlobalVariable *depth = new GlobalVariable(M, type_int, false, GlobalValue::ExternalLinkage, ConstantInt::get(type_int, 0), "depth");

    for (auto &F : M)
    {
        if (F.empty())
            continue;

        errs() << F.getName() << "\n";

        // 獲取該函數起頭的指令創建器
        BasicBlock &Bstart = F.front();
        Instruction &Istart = Bstart.front();
        IRBuilder<> BuilderStart(&Istart);

        // const char* name = functionName;
        Constant *name = BuilderStart.CreateGlobalStringPtr(F.getName());
        // printf("%*s%s: %p\n", depth, "", name, functionPtr);
        std::vector<llvm::Value *> args{format, depth, emptyStr, name, &F};
        BuilderStart.CreateCall(callee_printf, args);
        // depth += 1
        BuilderStart.CreateStore(BuilderStart.CreateAdd(depth, one), depth);

        // 獲取該函數結尾的指令創建器
        BasicBlock &Bend = F.back();
        Instruction &Iend = Bend.back();
        IRBuilder<> BuilderEnd(&Iend);

        // depth += -1
        BuilderEnd.CreateStore(BuilderEnd.CreateAdd(depth, negOne), depth);
    }

    return true;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);