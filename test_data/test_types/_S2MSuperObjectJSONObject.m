//
//  _S2MSuperObjectJSONObject.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import "S2MAPIParser.h"
#import "NSString+RegExValidation.h"
#import "S2MSuperObjectJSONObject.h"


@implementation _S2MSuperObjectJSONObject

#pragma mark - factory

+ (S2MSuperObjectJSONObject *)superObjectWithDictionary:(NSDictionary *)dic withError:(NSError **)error
{
    return [[S2MSuperObjectJSONObject alloc] initWithDictionary:dic withError:error];
}

#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error
{
    self = [super init];
    if (self) {
        self.isBoolean = [S2MAPIParser boolFromResponseDictionary:dic forKey:@"isBoolean" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        self.myData = [S2MAPIParser dataFromResponseDictionary:dic forKey:@"myData" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        self.creationDate = [S2MAPIParser dateWithTimeIntervalFromResponseDictionary:dic forKey:@"creationDate" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        self.objectWithoutSubtypes = [S2MAPIParser arrayFromResponseDictionary:dic forKey:@"objectWithoutSubtypes" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        NSArray *tmpNumbersArray = [S2MAPIParser arrayFromResponseDictionary:dic forKey:@"numbers" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        NSMutableArray *tmpNumbers = [[NSMutableArray alloc] initWithCapacity:tmpNumbersArray.count];
        for (NSUInteger loop = 0; loop < tmpNumbersArray.count; loop++) {
            NSNumber *tmpValue = [S2MAPIParser numberFromResponseArray:tmpNumbersArray atIndex:loop acceptNil:YES error:error];
            if (*error) {
                return self;
            }
            if (tmpValue) {
                [tmpNumbers addObject:tmpValue];
            }
        }
        self.numbers = [NSArray arrayWithArray:tmpNumbers];
        self.stringsAndDates = [S2MAPIParser arrayFromResponseDictionary:dic forKey:@"stringsAndDates" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        NSArray *tmpCustomNumbersArray = [S2MAPIParser arrayFromResponseDictionary:dic forKey:@"customNumbers" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        NSMutableArray *tmpCustomNumbers = [[NSMutableArray alloc] initWithCapacity:tmpCustomNumbersArray.count];
        for (NSUInteger loop = 0; loop < tmpCustomNumbersArray.count; loop++) {
            NSNumber *tmpValue = [S2MAPIParser numberFromResponseArray:tmpCustomNumbersArray atIndex:loop acceptNil:YES error:error];
            if (*error) {
                return self;
            }
            if (tmpValue) {
                [tmpCustomNumbers addObject:tmpValue];
            }
        }
        self.customNumbers = [NSArray arrayWithArray:tmpCustomNumbers];
        self.stringsAndCustomNumbers = [S2MAPIParser arrayFromResponseDictionary:dic forKey:@"stringsAndCustomNumbers" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
    }
    return self;
}

#pragma mark - getter

- (NSString *)stringInStringsAndDatesAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSString *tmpStringsAndDates = [S2MAPIParser stringFromResponseArray:self.stringsAndDates atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    return tmpStringsAndDates;
}

- (NSDate *)dateInStringsAndDatesAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSDate *tmpStringsAndDates = [S2MAPIParser dateWithTimeIntervalFromResponseArray:self.stringsAndDates atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    return tmpStringsAndDates;
}

- (NSNumber *)customNumberInStringsAndCustomNumbersAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSNumber *tmpStringsAndCustomNumbers = [S2MAPIParser numberFromResponseArray:self.stringsAndCustomNumbers atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    return tmpStringsAndCustomNumbers;
}

- (NSString *)stringInStringsAndCustomNumbersAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSString *tmpStringsAndCustomNumbers = [S2MAPIParser stringFromResponseArray:self.stringsAndCustomNumbers atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    return tmpStringsAndCustomNumbers;
}

#pragma mark - NSCoding

- (void)encodeWithCoder:(NSCoder*)coder
{
    [super encodeWithCoder:coder];
    [coder encodeBool:self.isBoolean forKey:@"isBoolean"];
    [coder encodeObject:self.myData forKey:@"myData"];
    [coder encodeObject:self.creationDate forKey:@"creationDate"];
    [coder encodeObject:self.objectWithoutSubtypes forKey:@"objectWithoutSubtypes"];
    [coder encodeObject:self.numbers forKey:@"numbers"];
    [coder encodeObject:self.stringsAndDates forKey:@"stringsAndDates"];
    [coder encodeObject:self.customNumbers forKey:@"customNumbers"];
    [coder encodeObject:self.stringsAndCustomNumbers forKey:@"stringsAndCustomNumbers"];
}

- (id)initWithCoder:(NSCoder *)coder
{
    self = [super initWithCoder:coder];
    self.isBoolean = [coder decodeBoolForKey:@"isBoolean"];
    self.myData = [coder decodeObjectForKey:@"myData"];
    self.creationDate = [coder decodeObjectForKey:@"creationDate"];
    self.objectWithoutSubtypes = [coder decodeObjectForKey:@"objectWithoutSubtypes"];
    self.numbers = [coder decodeObjectForKey:@"numbers"];
    self.stringsAndDates = [coder decodeObjectForKey:@"stringsAndDates"];
    self.customNumbers = [coder decodeObjectForKey:@"customNumbers"];
    self.stringsAndCustomNumbers = [coder decodeObjectForKey:@"stringsAndCustomNumbers"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary
{
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] init];
    if (self.isBoolean) {
        [dic setObject:[NSNumber numberWithBool:self.isBoolean] forKey:@"isBoolean"];
    }
    if (self.myData) {
        [dic setObject:self.myData forKey:@"myData"];
    }
    if (self.creationDate) {
        [dic setObject:[NSNumber numberWithInteger:[[NSNumber numberWithDouble:[self.creationDate timeIntervalSince1970]] longValue]] forKey:@"creationDate"];
    }
    if (self.objectWithoutSubtypes) {
        [dic setObject:self.objectWithoutSubtypes forKey:@"objectWithoutSubtypes"];
    }
    if (self.numbers) {
        [dic setObject:self.numbers forKey:@"numbers"];
    }
    if (self.stringsAndDates) {
        [dic setObject:self.stringsAndDates forKey:@"stringsAndDates"];
    }
    if (self.customNumbers) {
        [dic setObject:self.customNumbers forKey:@"customNumbers"];
    }
    if (self.stringsAndCustomNumbers) {
        [dic setObject:self.stringsAndCustomNumbers forKey:@"stringsAndCustomNumbers"];
    }
    return dic;
}

- (NSString *)description
{
    return [[self propertyDictionary] description];
}

@end
