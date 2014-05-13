//
//  _SenderGroupJSONObject.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@class SenderListJSONObject;
@class SenderList2JSONObject;

@class SenderGroupJSONObject;

@interface _SenderGroupJSONObject : NSObject <NSCoding>


// the array of sender list
@property (nonatomic, strong) NSArray *digitalSenders;
// the array of sender list
@property (nonatomic, strong) NSArray *HDOptions;
// the array of sender list
@property (nonatomic, strong) NSArray *DTVHighlights;
// the array of sender list
@property (nonatomic, strong) NSArray *IPTVSenders;

+ (SenderGroupJSONObject *)senderGroupWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;
- (SenderListJSONObject *)senderListInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error;
- (SenderList2JSONObject *)senderList2InDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error;
- (NSNumber *)numberInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error;
- (NSString *)stringInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error;
- (BOOL )booleanInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error;
- (NSDate *)dateInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error;
- (NSData *)dataInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error;
- (SenderListJSONObject *)senderListInHDOptionsAtIndex:(NSUInteger)index withError:(NSError **)error;
- (SenderList2JSONObject *)senderList2InHDOptionsAtIndex:(NSUInteger)index withError:(NSError **)error;
- (NSString *)stringInDTVHighlightsAtIndex:(NSUInteger)index withError:(NSError **)error;
- (NSString *)titleStringInDTVHighlightsAtIndex:(NSUInteger)index withError:(NSError **)error;
- (id)objectInIPTVSendersAtIndex:(NSUInteger)index withError:(NSError **)error;

@end
