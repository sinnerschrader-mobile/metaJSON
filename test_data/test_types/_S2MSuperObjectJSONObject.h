//
//  _S2MSuperObjectJSONObject.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@class S2MSuperObjectJSONObject;

@interface _S2MSuperObjectJSONObject : NSObject <NSCoding>


@property (nonatomic, assign) BOOL isBoolean;
@property (nonatomic, strong) NSData *myData;
@property (nonatomic, strong) NSDate *creationDate;
@property (nonatomic, strong) NSDate *updateDate;
@property (nonatomic, strong) NSArray *objectWithoutSubtypes;
@property (nonatomic, strong) NSArray *numbers;
@property (nonatomic, strong) NSArray *stringsAndDates;
@property (nonatomic, strong) NSArray *customNumbers;
@property (nonatomic, strong) NSArray *stringsAndCustomNumbers;

+ (S2MSuperObjectJSONObject *)superObjectWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;
- (NSString *)stringInStringsAndDatesAtIndex:(NSUInteger)index withError:(NSError **)error;
- (NSDate *)dateInStringsAndDatesAtIndex:(NSUInteger)index withError:(NSError **)error;
- (NSString *)stringInStringsAndCustomNumbersAtIndex:(NSUInteger)index withError:(NSError **)error;
- (NSNumber *)customNumberInStringsAndCustomNumbersAtIndex:(NSUInteger)index withError:(NSError **)error;

@end

