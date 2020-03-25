from eventextraction import EventsExtraction

extractor = EventsExtraction()
content = '虽然你做了坏事，但我觉得你是好人。一旦时机成熟，就坚决推行'
datas = extractor.extract_main(content)
print(datas)
