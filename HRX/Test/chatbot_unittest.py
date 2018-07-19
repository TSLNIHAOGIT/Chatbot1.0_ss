from HRX.Test.chatbot_model import models
import unittest
import HTMLTestRunner     # 导入HTMLTestRunner模块
# print(models()['IfKnowDebtor'].classify("不认识")['label'])

class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""

    def test_IfKnowDebtor(self):
        """Test method add(a, b)"""
        # self.assertEqual(1, models()['IfKnowDebtor'].classify("从没有听说过")['label'])
        # self.assertEqual(0, models()['IfKnowDebtor'].classify("认识")['label'])
        self.assertEqual(109, models()['IfKnowDebtor'].classify("今天天气真好")['label'])

    # def test_minus(self):
    #     """Test method minus(a, b)"""
    #     self.assertEqual(1, minus(3, 2))
    #
    # def test_multi(self):
    #     """Test method multi(a, b)"""
    #     self.assertEqual(6, multi(2, 3))
    #
    # def test_divide(self):
    #     """Test method divide(a, b)"""
    #     self.assertEqual(2, divide(6, 3))
    #     self.assertEqual(2.5, divide(5, 2))

if __name__ == '__main__':
    unittest.main()


    # fp = open('a.html','wb')
    #
    # runner = HTMLTestRunner.HTMLTestRunner(
    #     stream=fp,
    #     title=u'搜索功能测试报告',
    #     description=u'用例执行情况：')
    # # 关闭文件流，不关的话生成的报告是空的
    # fp.close()
    #
    # runner.run(unittest.main())

