module LibSpec
    ( spec
    ) where

import Test.Hspec
import Lib (add, subtract, multiply, divide, calculate)

spec :: Spec
spec = do
    describe "add" $ do
        it "adds two positive numbers" $ do
            add 2 3 `shouldBe` 5.0

        it "adds negative numbers" $ do
            add (-2) (-3) `shouldBe` (-5.0)

        it "adds positive and negative numbers" $ do
            add 5 (-3) `shouldBe` 2.0

    describe "subtract" $ do
        it "subtracts two positive numbers" $ do
            subtract 5 3 `shouldBe` 2.0

        it "subtracts negative numbers" $ do
            subtract (-2) (-3) `shouldBe` 1.0

    describe "multiply" $ do
        it "multiplies two positive numbers" $ do
            multiply 3 4 `shouldBe` 12.0

        it "multiplies by zero" $ do
            multiply 5 0 `shouldBe` 0.0

        it "multiplies negative numbers" $ do
            multiply (-2) 3 `shouldBe` (-6.0)

    describe "divide" $ do
        it "divides two positive numbers" $ do
            divide 12 3 `shouldBe` Right 4.0

        it "handles decimal results" $ do
            divide 5 2 `shouldBe` Right 2.5

        it "returns error for division by zero" $ do
            divide 5 0 `shouldBe` Left "Division by zero"

    describe "calculate" $ do
        it "performs addition" $ do
            calculate "+" 2 3 `shouldBe` Right 5.0

        it "performs subtraction" $ do
            calculate "-" 5 3 `shouldBe` Right 2.0

        it "performs multiplication" $ do
            calculate "*" 3 4 `shouldBe` Right 12.0

        it "performs division" $ do
            calculate "/" 12 3 `shouldBe` Right 4.0

        it "returns error for unknown operation" $ do
            calculate "%" 5 3 `shouldBe` Left "Unknown operation"

        it "returns error for division by zero" $ do
            calculate "/" 5 0 `shouldBe` Left "Division by zero"
