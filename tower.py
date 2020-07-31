def Tower(size, fromStack, toStack, spareStack):
    if size == 1:
        print 'Move disk from ',fromStack,'to ',toStack
    else:
        Tower(size - 1, fromStack, spareStack, toStack)
        Tower(1, fromStack, toStack, spareStack)
        Tower(size - 1, spareStack, toStack, fromStack)
