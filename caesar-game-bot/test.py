import dataBase as db

text = 'a1 d3'
text2 = 's1, f4, g2, g1'
text3 = ',,,,,,,,,s1,,,,,,f4 ,,  ,, , , ,, h6'

print(db.answerProcessing(text))
print(db.answerProcessing(text2))
print(db.answerProcessing(text3))