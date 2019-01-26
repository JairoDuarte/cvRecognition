from cvanalyse.utils import Converter, DataPreProcess


class Store():

    @staticmethod
    def getCV(filePath):
        """
        Lit le cv selon son format
        :param self:
        :param fileName:
        :return:
        """

        extension = filePath.split(".")[-1]

        if extension == 'txt':
            try:
                file = open(filePath, 'r')
                content = file.read()
                file.close()
            except Exception as e:
                print(e)
                pass

            return DataPreProcess.process(content)

        elif extension == 'docx':
            content =  Converter.docxToText(filePath)
            return DataPreProcess.process(content)

        elif extension == 'pdf':
            content = Converter.pdfToText(filePath)
            return DataPreProcess.process(content)

        else:
            print('Le format du fichier n\'est pas supporté')
