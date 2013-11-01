//
//  NSString+RegExValidation.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@interface NSString (RegExValidation)

#define emailRegex @"^[_a-z0-9-]+(\\.[_a-z0-9-]+)*@[a-z0-9-]+(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$"

- (NSUInteger) numberOfMatchesWithRegExString:(NSString *)regExString;

- (BOOL) matchesRegExString:(NSString *)regExString;

- (BOOL) isValidEmailFormatString;
@end
