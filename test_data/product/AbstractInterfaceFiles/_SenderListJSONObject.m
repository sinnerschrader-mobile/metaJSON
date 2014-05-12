//
//  _SenderListJSONObject.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import "APIParser.h"
#import "NSString+RegExValidation.h"
#import "SenderListJSONObject.h"
#import "SenderJSONObject.h"


@implementation _SenderListJSONObject

#pragma mark - factory

+ (SenderListJSONObject *)senderListWithDictionary:(NSDictionary *)dic withError:(NSError **)error
{
    return [[SenderListJSONObject alloc] initWithDictionary:dic withError:error];
}


#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error
{
    self = [super init];
    if (self) {
        self.listTitle = [APIParser stringFromResponseDictionary:dic forKey:@"listTitle" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        NSArray *tmpSendersArray = [APIParser arrayFromResponseDictionary:dic forKey:@"senders" acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        NSMutableArray *tmpSenders = [[NSMutableArray alloc] initWithCapacity:tmpSendersArray.count];
        for (NSUInteger loop = 0; loop < tmpSendersArray.count; loop++) {
            NSDictionary *tmpDic = [APIParser dictionaryFromResponseArray:tmpSendersArray atIndex:loop acceptNil:NO error:error];
            if (*error) {
                return self;
            }
            SenderJSONObject*tmpObject = nil;
            if (tmpDic) {
                tmpObject= [[SenderJSONObject alloc] initWithDictionary:tmpDic withError:error];
                if (*error) {
                    return self;
                }
            }
            if (tmpObject) {
                [tmpSenders addObject:tmpObject];
            }
        }
        self.senders = [NSArray arrayWithArray:tmpSenders];
    }
    return self;
}


#pragma mark - getter

#pragma mark - NSCoding
- (void)encodeWithCoder:(NSCoder*)coder
{
    [super encodeWithCoder:coder];
    [coder encodeObject:self.listTitle forKey:@"listTitle"];
    [coder encodeObject:self.senders forKey:@"senders"];
}
- (id)initWithCoder:(NSCoder *)coder
{
    self = [super initWithCoder:coder];
    self.listTitle = [coder decodeObjectForKey:@"listTitle"];
    self.senders = [coder decodeObjectForKey:@"senders"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary
{
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] init];
    if (self.listTitle) {
        [dic setObject:self.listTitle forKey:@"listTitle"];
    }
    if (self.senders) {
        NSMutableArray *tmpArray = [[NSMutableArray alloc] init];
        for (SenderJSONObject *tmpObj in self.senders) {
            [tmpArray addObject:[tmpObj propertyDictionary]];
        }
        [dic setObject:tmpArray forKey:@"senders"];
    }
    return dic;
}
- (NSString *)description
{
    return [[self propertyDictionary] description];
}

@end
