//
//  NSString+RegExValidation.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import "NSString+RegExValidation.h"

@implementation NSString (RegExValidation)

- (NSUInteger) numberOfMatchesWithRegExString:(NSString *)regExString {
    if (regExString == nil || [regExString isKindOfClass:[NSString class]] == NO || regExString.length == 0) {
        return 0;
    }
    NSError *error = nil;
    NSRegularExpression *regex = [NSRegularExpression regularExpressionWithPattern:regExString options:NSRegularExpressionCaseInsensitive error:&error];
    if (error) {
        NSLog(@"Regular expression match error : %@", error);
        return 0;
    }
    return [regex numberOfMatchesInString:self options:0 range:NSMakeRange(0, self.length)];
}

- (BOOL) matchesRegExString:(NSString *)regExString {
    return ([self numberOfMatchesWithRegExString:regExString] > 0);
}

- (BOOL) isValidEmailFormatString {
    return [self matchesRegExString:emailRegex];
}

@end
